const messagesEl = document.getElementById('messages');
const inputEl = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');

function appendMessage(text, who='bot', meta=''){
  const wrap = document.createElement('div');
  wrap.className = 'msg ' + (who === 'user' ? 'user' : 'bot');
  wrap.innerHTML = `<div class="text">${escapeHtml(text)}</div>` + (meta?`<div class="meta">${escapeHtml(meta)}</div>`:'');
  messagesEl.appendChild(wrap);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function escapeHtml(unsafe) {
  return unsafe
       .replace(/&/g, "&amp;")
       .replace(/</g, "&lt;")
       .replace(/>/g, "&gt;")
       .replace(/"/g, "&quot;")
       .replace(/'/g, "&#039;");
}

async function sendMessage(){
  const text = inputEl.value.trim();
  if(!text) return;
  appendMessage(text, 'user');
  inputEl.value = '';
  appendMessage('Thinking...', 'bot', '...');

  try{
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });

    const data = await res.json();
    // Remove the 'Thinking...' placeholder
    const last = messagesEl.querySelector('.msg.bot:last-child');
    if(last && last.innerText.includes('Thinking')) last.remove();

    if(res.ok && data.response){
      appendMessage(data.response, 'bot', data.metadata ? `Model: ${data.metadata.model_used} • ${data.metadata.response_time.toFixed(2)}s` : '');
    } else {
      appendMessage(data.error || 'Server error', 'bot');
    }
  }catch(err){
    appendMessage('Network error: ' + err.message, 'bot');
  }
}

sendBtn.addEventListener('click', sendMessage);
inputEl.addEventListener('keydown', (e)=>{ if(e.key === 'Enter'){ sendMessage(); } });

// initial welcome
appendMessage("Hello! This is the Ultra-Advanced Kiosk Chatbot. Ask me anything.", 'bot');
