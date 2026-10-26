(() => {
  'use strict';
  const $ = (selector) => document.querySelector(selector);
  const state = {
    status: null,
    busy: false,
    voiceOutput: localStorage.getItem('robotVoiceOutput') === 'true',
    accessToken: localStorage.getItem('robotAccessToken') || '',
    recognition: null,
  };

  const el = {
    provider: $('#providerState'), model: $('#modelState'), memory: $('#memoryState'),
    connectionPill: $('#connectionPill'), connectionLabel: $('#connectionLabel'),
    setupBanner: $('#setupBanner'), messages: $('#messages'), empty: $('#emptyState'),
    composer: $('#composer'), input: $('#messageInput'), send: $('#sendButton'), count: $('#charCount'),
    pending: $('#pendingMessage'), errors: $('#errorBanner'), avatar: $('#avatarStage'), mood: $('#avatarMood'),
    accessOverlay: $('#accessOverlay'), accessForm: $('#accessForm'), accessInput: $('#accessInput'), accessError: $('#accessError'),
    settingsOverlay: $('#settingsOverlay'), toast: $('#toast'), voiceOutput: $('#voiceOutputButton'), settingsVoice: $('#settingsVoiceToggle'),
  };

  function setConnection(label, type = '') {
    el.connectionLabel.textContent = label;
    el.connectionPill.classList.toggle('connected', type === 'connected');
    el.connectionPill.classList.toggle('error', type === 'error');
  }

  function showError(message) {
    el.errors.textContent = message;
    el.errors.hidden = false;
  }
  function clearError() { el.errors.hidden = true; el.errors.textContent = ''; }

  async function api(path, options = {}) {
    const headers = new Headers(options.headers || {});
    headers.set('Accept', 'application/json');
    if (options.body) headers.set('Content-Type', 'application/json');
    if (state.accessToken) headers.set('Authorization', `Bearer ${state.accessToken}`);
    const response = await fetch(path, { ...options, headers, cache: 'no-store' });
    let data;
    try { data = await response.json(); } catch { data = {}; }
    if (response.status === 401) {
      el.accessOverlay.hidden = false;
      el.accessError.textContent = 'That key was not accepted. Check the server configuration and try again.';
      el.accessError.hidden = false;
      throw new Error('Access key required.');
    }
    if (!response.ok) throw new Error(data.error || `Request failed (${response.status}).`);
    return data;
  }

  function syncVoiceButtons() {
    el.voiceOutput.classList.toggle('active', state.voiceOutput);
    el.voiceOutput.setAttribute('aria-pressed', String(state.voiceOutput));
    el.voiceOutput.querySelector('span').textContent = state.voiceOutput ? 'Voice on' : 'Voice off';
    el.settingsVoice.setAttribute('aria-checked', String(state.voiceOutput));
    if (!el.settingsVoice.querySelector('span')) el.settingsVoice.append(document.createElement('span'));
  }

  function updateComposer() {
    const length = el.input.value.length;
    el.count.textContent = `${length} / 4000`;
    const canSend = Boolean(state.status && state.status.ai_configured && !state.busy && el.input.value.trim());
    el.send.disabled = !canSend;
    el.input.disabled = Boolean(state.busy);
  }

  function renderHistory(messages) {
    el.messages.querySelectorAll('.message-row').forEach((node) => node.remove());
    const realMessages = Array.isArray(messages) ? messages.filter((m) => ['user', 'assistant'].includes(m.role) && typeof m.content === 'string') : [];
    el.empty.hidden = realMessages.length > 0;
    realMessages.forEach((message) => appendMessage(message.role, message.content, false));
    scrollMessages();
    el.memory.textContent = `${realMessages.length} MSG${realMessages.length === 1 ? '' : 'S'}`;
  }

  function appendMessage(role, text, shouldSpeak = false) {
    el.empty.hidden = true;
    const row = document.createElement('article');
    row.className = `message-row ${role}`;
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? 'YOU' : 'AI';
    const body = document.createElement('div');
    body.className = 'message-body';
    const meta = document.createElement('div');
    meta.className = 'message-meta';
    const who = document.createElement('span');
    who.textContent = role === 'user' ? 'YOU' : 'VIRTUAL AI';
    const when = document.createElement('span');
    when.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    meta.append(who, when);
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = text;
    body.append(meta, bubble);
    row.append(avatar, body);
    el.messages.append(row);
    scrollMessages();
    if (shouldSpeak && state.voiceOutput) speak(text);
  }

  function scrollMessages() { el.messages.scrollTop = el.messages.scrollHeight; }

  function speak(text) {
    if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
      showToast('Spoken replies are not supported in this browser.');
      return;
    }
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  function showToast(message) {
    el.toast.textContent = message;
    el.toast.hidden = false;
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => { el.toast.hidden = true; }, 3000);
  }

  async function loadStatus() {
    setConnection('Connecting');
    try {
      state.status = await api('/api/status');
      clearError();
      const configured = Boolean(state.status.ai_configured);
      el.provider.textContent = configured ? 'Configured' : 'Not connected';
      el.provider.style.color = configured ? 'var(--green)' : 'var(--danger)';
      el.model.textContent = state.status.model || '—';
      el.setupBanner.hidden = configured;
      setConnection(configured ? 'Provider configured' : 'AI setup required', configured ? 'connected' : 'error');
      if (state.status.requires_access_token) {
        try { await api('/api/history'); }
        catch (error) { if (/Access key required/.test(error.message)) el.accessOverlay.hidden = false; }
      }
      if (!state.status.requires_access_token || state.accessToken) {
        try { const data = await api('/api/history'); renderHistory(data.messages); }
        catch (error) { if (!/Access key required/.test(error.message)) throw error; }
      }
      if (!configured) el.mood.textContent = 'AWAITING AI LINK';
      else el.mood.textContent = 'PROVIDER READY';
      updateComposer();
    } catch (error) {
      setConnection('Server unavailable', 'error');
      el.provider.textContent = 'Offline';
      el.model.textContent = '—';
      el.mood.textContent = 'LINK OFFLINE';
      showError(`Cannot connect to the virtual AI server: ${error.message} Ensure the Python server is running and reopen this page.`);
    }
  }

  async function submitMessage(text) {
    if (state.busy || !text.trim()) return;
    if (!state.status || !state.status.ai_configured) {
      showError('No real AI provider is configured. Set OPENAI_API_KEY on the server; this app will not invent a response.');
      return;
    }
    clearError();
    state.busy = true;
    let succeeded = false;
    el.pending.hidden = false;
    el.avatar.classList.add('thinking');
    el.mood.textContent = 'THINKING';
    updateComposer();
    try {
      const result = await api('/api/chat', { method: 'POST', body: JSON.stringify({ message: text.trim() }) });
      renderHistory(result.messages);
      succeeded = true;
      if (!Array.isArray(result.messages)) appendMessage('assistant', result.reply, true);
      else if (state.voiceOutput && result.reply) speak(result.reply);
      el.mood.textContent = 'READY';
      setConnection('Session active', 'connected');
    } catch (error) {
      showError(error.message);
      el.mood.textContent = state.status && state.status.ai_configured ? 'RETRY REQUIRED' : 'AWAITING AI LINK';
    } finally {
      state.busy = false;
      el.pending.hidden = true;
      el.avatar.classList.remove('thinking');
      if (succeeded) el.input.value = '';
      autoResizeInput();
      updateComposer();
      el.input.focus();
    }
  }

  function autoResizeInput() {
    el.input.style.height = 'auto';
    el.input.style.height = `${Math.min(el.input.scrollHeight, 150)}px`;
    updateComposer();
  }

  el.composer.addEventListener('submit', (event) => {
    event.preventDefault();
    submitMessage(el.input.value);
  });
  el.input.addEventListener('input', autoResizeInput);
  el.input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      if (!el.send.disabled) el.composer.requestSubmit();
    }
  });
  document.querySelectorAll('[data-prompt]').forEach((button) => button.addEventListener('click', () => {
    el.input.value = button.getAttribute('data-prompt') || '';
    autoResizeInput();
    el.input.focus();
  }));

  $('#clearButton').addEventListener('click', async () => {
    if (!window.confirm('Clear the shared conversation for every connected device?')) return;
    try {
      await api('/api/reset', { method: 'POST', body: '{}' });
      renderHistory([]);
      clearError();
      showToast('Shared conversation cleared.');
    } catch (error) { showError(error.message); }
  });

  function toggleVoiceOutput() {
    state.voiceOutput = !state.voiceOutput;
    localStorage.setItem('robotVoiceOutput', String(state.voiceOutput));
    if (!state.voiceOutput && 'speechSynthesis' in window) window.speechSynthesis.cancel();
    syncVoiceButtons();
    showToast(state.voiceOutput ? 'Spoken replies enabled on this device.' : 'Spoken replies disabled on this device.');
  }
  el.voiceOutput.addEventListener('click', toggleVoiceOutput);
  el.settingsVoice.addEventListener('click', toggleVoiceOutput);

  $('#settingsButton').addEventListener('click', () => { el.settingsOverlay.hidden = false; });
  $('#closeSettings').addEventListener('click', () => { el.settingsOverlay.hidden = true; });
  $('#settingsDone').addEventListener('click', () => { el.settingsOverlay.hidden = true; });
  el.settingsOverlay.addEventListener('click', (event) => { if (event.target === el.settingsOverlay) el.settingsOverlay.hidden = true; });

  el.accessForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const token = el.accessInput.value.trim();
    if (!token) return;
    state.accessToken = token;
    localStorage.setItem('robotAccessToken', token);
    el.accessError.hidden = true;
    try {
      const data = await api('/api/history');
      renderHistory(data.messages);
      el.accessOverlay.hidden = true;
      el.accessInput.value = '';
      showToast('Connected to the shared AI session.');
    } catch (error) {
      if (/Access key required/.test(error.message)) {
        localStorage.removeItem('robotAccessToken');
        state.accessToken = '';
      }
      el.accessError.textContent = error.message;
      el.accessError.hidden = false;
    }
  });

  $('#micButton').addEventListener('click', () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      showToast('Voice input is not supported by this browser. You can still type messages.');
      return;
    }
    if (state.recognition) {
      state.recognition.stop();
      state.recognition = null;
      $('#micButton').classList.remove('active');
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = navigator.language || 'en-US';
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;
    const startingText = el.input.value;
    recognition.onstart = () => { $('#micButton').classList.add('active'); showToast('Listening on this device…'); };
    recognition.onresult = (event) => {
      let interim = '';
      let finalText = '';
      for (let i = event.resultIndex; i < event.results.length; i += 1) {
        const transcript = event.results[i][0].transcript;
        if (event.results[i].isFinal) finalText += transcript;
        else interim += transcript;
      }
      el.input.value = `${startingText}${startingText && finalText ? ' ' : ''}${finalText || interim}`;
      autoResizeInput();
    };
    recognition.onerror = (event) => showToast(`Microphone error: ${event.error}. Check browser permission.`);
    recognition.onend = () => { state.recognition = null; $('#micButton').classList.remove('active'); el.input.focus(); };
    state.recognition = recognition;
    try { recognition.start(); } catch { state.recognition = null; showToast('Could not start microphone. Check permissions.'); }
  });

  syncVoiceButtons();
  updateComposer();
  loadStatus();
  // Poll the shared history so a message sent from another device appears here.
  window.setInterval(async () => {
    if (document.hidden || state.busy || el.accessOverlay.hidden === false) return;
    try {
      const data = await api('/api/history');
      const displayed = Array.from(el.messages.querySelectorAll('.message-row')).map((row) => ({
        role: row.classList.contains('user') ? 'user' : 'assistant',
        content: row.querySelector('.message-bubble')?.textContent || '',
      }));
      const incoming = Array.isArray(data.messages) ? data.messages : [];
      if (JSON.stringify(displayed) !== JSON.stringify(incoming)) renderHistory(incoming);
      if (state.status && incoming.length !== state.status.conversation_messages) {
        state.status.conversation_messages = incoming.length;
        el.memory.textContent = `${incoming.length} MSG${incoming.length === 1 ? '' : 'S'}`;
      }
    } catch (error) {
      if (!/Access key required/.test(error.message)) setConnection('Sync interrupted', 'error');
    }
  }, 4000);
})();
