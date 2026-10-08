/**
 * SkillSwap DNA - Neo-Brutalist AJAX Form & Action Handlers
 * Converts all mutation requests into seamless asynchronous AJAX calls.
 */

// Global Neo-Brutalist Toast System
function showNeoToast(message, type = 'success') {
  let toastContainer = document.getElementById('neo-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'neo-toast-container';
    toastContainer.className = 'fixed top-5 right-5 z-[9999] flex flex-col gap-2 pointer-events-none max-w-sm w-full';
    document.body.appendChild(toastContainer);
  }

  const bgColors = {
    success: 'bg-[#dcfce7] text-slate-900',
    error: 'bg-[#ffe4e6] text-slate-900',
    info: 'bg-[#fef08a] text-slate-900',
    pod: 'bg-[#f3e8ff] text-slate-900'
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    pod: '🔄'
  };

  const toast = document.createElement('div');
  toast.className = `pointer-events-auto p-3.5 px-5 rounded-full border-2 border-slate-900 ${bgColors[type] || bgColors.success} font-bold text-xs shadow-[3px_3px_0px_0px_#0f172a] flex items-center justify-between gap-3 transform translate-y-[-10px] opacity-0 transition-all duration-200`;
  toast.innerHTML = `
    <div class="flex items-center gap-2">
      <span class="w-5 h-5 rounded-full bg-white border border-slate-900 flex items-center justify-center font-black text-[10px]">${icons[type] || '✓'}</span>
      <span>${message}</span>
    </div>
    <button onclick="this.parentElement.remove()" class="text-slate-900 font-extrabold hover:opacity-75">✕</button>
  `;

  toastContainer.appendChild(toast);

  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-[-10px]', 'opacity-0');
    toast.classList.add('translate-y-0', 'opacity-100');
  });

  // Auto-remove after 3.5s
  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-[-10px]');
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

// Increments the Karma Badge in navbar with a bounce pop
function updateNavKarma(amount = 20) {
  const karmaPill = document.querySelector('header a[href*="profile"] span, header button img + span');
  if (karmaPill) {
    const current = parseInt(karmaPill.innerText) || 0;
    karmaPill.innerText = `${current + amount} pts`;
    
    // Scale bounce
    karmaPill.parentElement.style.transition = 'transform 0.25s cubic-bezier(0.34, 1.56, 0.64, 1)';
    karmaPill.parentElement.style.transform = 'scale(1.22)';
    setTimeout(() => {
      karmaPill.parentElement.style.transform = 'scale(1)';
    }, 280);
  }
}

// Spawns celebratory floating karma particles
function spawnKarmaBurst(targetElement, karmaAmount = 20) {
  if (!targetElement) return;
  const rect = targetElement.getBoundingClientRect();
  const particles = [
    { text: `+${karmaAmount} Points! 🌟`, color: 'text-amber-500 bg-[#fef08a]', size: 'text-xs sm:text-sm' },
    { text: 'Barter Verified! 🧬', color: 'text-emerald-700 bg-[#dcfce7]', size: 'text-[11px]' },
    { text: 'Level Up! 🚀', color: 'text-purple-700 bg-[#f3e8ff]', size: 'text-[11px]' }
  ];

  particles.forEach((p, idx) => {
    setTimeout(() => {
      const el = document.createElement('div');
      el.className = `karma-float-particle ${p.color} ${p.size} px-3 py-1 rounded-full border-2 border-slate-900 shadow-[2px_2px_0px_0px_#0f172a] font-black z-[9999]`;
      el.innerText = p.text;
      el.style.left = `${rect.left + rect.width / 2 - 40 + (idx * 24 - 24)}px`;
      el.style.top = `${rect.top + window.scrollY - 15}px`;
      document.body.appendChild(el);

      setTimeout(() => el.remove(), 1450);
    }, idx * 140);
  });
}

document.addEventListener('DOMContentLoaded', function () {
  
  // 1. Intercept Swap Request Modal Form
  const swapModal = document.getElementById('swap-modal');
  if (swapModal) {
    const swapForm = swapModal.querySelector('form');
    if (swapForm) {
      swapForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const submitBtn = swapForm.querySelector('button[type="submit"]');
        const origText = submitBtn.innerText;
        submitBtn.disabled = true;
        submitBtn.innerText = 'Sending...';

        const formData = new FormData(swapForm);
        fetch('/exchanges/create', {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
          .then(res => res.json())
          .then(data => {
            submitBtn.disabled = false;
            submitBtn.innerText = origText;
            if (data.success) {
              const stamp = document.getElementById('swap-stamp-container');
              if (stamp) stamp.classList.remove('hidden');
              showNeoToast('🎉 Barter request sent to your peer!', 'success');
              setTimeout(() => {
                if (typeof closeSwapModal === 'function') closeSwapModal();
                swapForm.reset();
              }, 700);
            } else {
              showNeoToast(data.error || 'Failed to send request.', 'error');
            }
          })
          .catch(err => {
            submitBtn.disabled = false;
            submitBtn.innerText = origText;
            showNeoToast('Error connecting to server.', 'error');
          });
      });
    }
  }

  // 2. Intercept Pod Launch Forms
  document.querySelectorAll('form[action*="/exchanges/create"]').forEach(form => {
    const typeInput = form.querySelector('input[name="type"]');
    if (typeInput && typeInput.value === 'pod') {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.innerText = 'Launching Pod...';

        const formData = new FormData(form);
        fetch('/exchanges/create', {
          method: 'POST',
          body: formData,
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              submitBtn.innerText = '✓ Pod Launched!';
              submitBtn.classList.add('bg-emerald-600');
              showNeoToast('🚀 Circular 3-Way Pod formed successfully!', 'pod');
            } else {
              submitBtn.disabled = false;
              submitBtn.innerText = 'Launch Pod';
              showNeoToast(data.error || 'Failed to form pod.', 'error');
            }
          })
          .catch(() => {
            submitBtn.disabled = false;
            submitBtn.innerText = 'Launch Pod';
            showNeoToast('Error forming pod.', 'error');
          });
      });
    }
  });

  // 3. Intercept Session Complete & Exchange Action Forms
  document.querySelectorAll('form[action*="/exchanges/action/"]').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const actionInput = form.querySelector('input[name="action"]');
      const action = actionInput ? actionInput.value : '';
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            if (action === 'complete_session') {
              // Update progress bar in place
              const card = form.closest('.card-mint, .card-purple, .drizzle-card');
              if (card) {
                const progressFill = card.querySelector('.bg-slate-900, .bg-gradient-to-r');
                const progressText = card.querySelector('span:has-text("Done"), span:has-text("Completed")') || card.querySelectorAll('span')[2];
                if (progressFill && data.total_sessions) {
                  const pct = Math.round((data.completed_sessions / data.total_sessions) * 100);
                  progressFill.style.width = pct + '%';
                }
                const progressSpan = card.querySelector('.font-black.text-slate-800 span:last-child');
                if (progressSpan) {
                  progressSpan.innerText = `${data.completed_sessions} of ${data.total_sessions} Done`;
                }
              }
              updateNavKarma(20);
              spawnKarmaBurst(submitBtn, 20);
              showNeoToast(`⭐ Session ${data.completed_sessions}/${data.total_sessions} Complete! +20 Points added.`, 'success');
              if (submitBtn) {
                submitBtn.disabled = false;
                if (data.status === 'completed') {
                  submitBtn.innerText = '✓ All Sessions Completed';
                  submitBtn.disabled = true;
                }
              }
            } else if (action === 'accept') {
              showNeoToast('✅ Swap request accepted! Ready to coordinate.', 'success');
              const card = form.closest('.card-yellow, .drizzle-card');
              if (card) {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.95)';
                setTimeout(() => card.remove(), 300);
              }
            } else if (action === 'reject') {
              showNeoToast('Swap declined.', 'info');
              const card = form.closest('.card-yellow, .drizzle-card');
              if (card) {
                card.remove();
              }
            } else if (action === 'update_schedule') {
              showNeoToast('📅 Schedule details updated.', 'success');
              if (typeof closeScheduleModal === 'function') closeScheduleModal();
            }
          } else {
            showNeoToast(data.error || 'Action failed.', 'error');
            if (submitBtn) submitBtn.disabled = false;
          }
        })
        .catch(() => {
          showNeoToast('Connection error.', 'error');
          if (submitBtn) submitBtn.disabled = false;
        });
    });
  });

  // 4. Intercept Direct Messaging Chat Form
  const chatForm = document.querySelector('form[action*="/messages/send"]');
  if (chatForm) {
    chatForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const textInput = chatForm.querySelector('input[name="text"]');
      const textVal = textInput.value.trim();
      if (!textVal) return;

      const submitBtn = chatForm.querySelector('button[type="submit"]');
      if (submitBtn) submitBtn.disabled = true;

      const formData = new FormData(chatForm);
      fetch(chatForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          if (submitBtn) submitBtn.disabled = false;
          if (data.success) {
            textInput.value = '';
            // Append new message bubble
            const chatScroll = document.querySelector('.overflow-y-auto.space-y-4');
            if (chatScroll) {
              const bubbleWrapper = document.createElement('div');
              bubbleWrapper.className = 'flex justify-end';
              bubbleWrapper.innerHTML = `
                <div class="max-w-md space-y-1">
                  <div class="p-3.5 rounded-2xl bg-[#dcfce7] border-2 border-slate-900 text-slate-900 text-xs font-bold shadow-[2px_2px_0px_0px_#0f172a]">
                    ${data.message.text}
                  </div>
                  <div class="text-[10px] text-slate-500 text-right font-semibold">Just now</div>
                </div>
              `;
              chatScroll.appendChild(bubbleWrapper);
              chatScroll.scrollTop = chatScroll.scrollHeight;
            }
          }
        })
        .catch(() => {
          if (submitBtn) submitBtn.disabled = false;
          showNeoToast('Failed to send message.', 'error');
        });
    });
  }

  // 5. Intercept Follow/Unfollow Button Forms
  document.querySelectorAll('form[action*="/follow"]').forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const btn = form.querySelector('button');
      btn.disabled = true;

      fetch(form.action, {
        method: 'POST',
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          btn.disabled = false;
          if (data.success) {
            btn.innerText = data.is_following ? 'Following ✓' : '+ Follow';
            showNeoToast(data.message, 'success');
          }
        })
        .catch(() => {
          btn.disabled = false;
          showNeoToast('Network error.', 'error');
        });
    });
  });

  // 6. Intercept Add Skill Form (in Profile)
  const addSkillForms = document.querySelectorAll('form[action*="/profile/skill/add"]');
  addSkillForms.forEach(form => {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;

      const formData = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          submitBtn.disabled = false;
          if (data.success) {
            showNeoToast(data.message, 'success');
            form.reset();
            // Prepend new skill card to container
            const container = form.parentElement.querySelector('.space-y-2\\.5, .space-y-3');
            if (container && data.skill) {
              const skillCard = document.createElement('div');
              skillCard.className = 'p-3 rounded-2xl bg-white border-2 border-slate-900 flex items-center justify-between gap-3 shadow-[2px_2px_0px_0px_#0f172a]';
              skillCard.innerHTML = `
                <div class="text-xs font-bold">
                  <div class="text-slate-900 font-extrabold">${data.skill.name}</div>
                  <div class="text-slate-500 text-[11px]">${data.skill.level || data.skill.target_level} &bull; ${data.skill.category}</div>
                </div>
                <form action="/profile/skill/delete/${data.skill_type}/${data.skill.id}" method="POST">
                  <button type="submit" class="w-7 h-7 rounded-full border border-slate-900 bg-rose-100 hover:bg-rose-200 text-rose-700 flex items-center justify-center font-bold text-xs">✕</button>
                </form>
              `;
              container.prepend(skillCard);
            }
          } else {
            showNeoToast(data.error || 'Failed to add skill.', 'error');
          }
        })
        .catch(() => {
          submitBtn.disabled = false;
          showNeoToast('Error adding skill.', 'error');
        });
  // 7. Intercept Student Sign In Form (Login)
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const submitBtn = document.getElementById('login-submit-btn') || loginForm.querySelector('button[type="submit"]');
      const errContainer = document.getElementById('login-error-container');
      const origText = submitBtn.innerHTML;

      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Verifying Credentials...</span>';
      if (errContainer) {
        errContainer.classList.add('hidden');
        errContainer.innerText = '';
      }

      const formData = new FormData(loginForm);
      fetch(loginForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showNeoToast(data.message || 'Signed in successfully!', 'success');
            submitBtn.innerHTML = '<span>✓ Signed In!</span>';
            setTimeout(() => {
              window.location.href = data.redirect || '/';
            }, 400);
          } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = origText;
            const errMsg = data.error || 'Invalid credentials.';
            if (errContainer) {
              errContainer.innerText = errMsg;
              errContainer.classList.remove('hidden');
            }
            showNeoToast(errMsg, 'error');
          }
        })
        .catch(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = origText;
          const errMsg = 'Network error during sign in.';
          if (errContainer) {
            errContainer.innerText = errMsg;
            errContainer.classList.remove('hidden');
          }
          showNeoToast(errMsg, 'error');
        });
    });
  }

  // 8. Intercept Student Registration Form (Register)
  const registerForm = document.getElementById('register-form');
  if (registerForm) {
    registerForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const submitBtn = document.getElementById('register-submit-btn') || registerForm.querySelector('button[type="submit"]');
      const errContainer = document.getElementById('register-error-container');
      const origText = submitBtn.innerHTML;

      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span>Creating DNA Profile...</span>';
      if (errContainer) {
        errContainer.classList.add('hidden');
        errContainer.innerText = '';
      }

      const formData = new FormData(registerForm);
      fetch(registerForm.action, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showNeoToast(data.message || 'Account created! Welcome to SkillSwap DNA.', 'success');
            submitBtn.innerHTML = '<span>✓ DNA Configured! Redirecting...</span>';
            setTimeout(() => {
              window.location.href = data.redirect || '/';
            }, 500);
          } else {
            submitBtn.disabled = false;
            submitBtn.innerHTML = origText;
            const errMsg = data.error || 'Failed to create account.';
            if (errContainer) {
              errContainer.innerText = errMsg;
              errContainer.classList.remove('hidden');
            }
            showNeoToast(errMsg, 'error');
          }
        })
        .catch(() => {
          submitBtn.disabled = false;
          submitBtn.innerHTML = origText;
          const errMsg = 'Network error during registration.';
          if (errContainer) {
            errContainer.innerText = errMsg;
            errContainer.classList.remove('hidden');
          }
          showNeoToast(errMsg, 'error');
        });
    });
  }

  // 9. Intercept Demo Login Quick Buttons
  document.querySelectorAll('.demo-login-btn').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const href = this.getAttribute('href');
      if (!href) return;

      showNeoToast('Signing into demo persona...', 'info');
      fetch(href, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showNeoToast(data.message || 'Demo session activated!', 'success');
            setTimeout(() => {
              window.location.href = data.redirect || '/';
            }, 300);
          } else {
            window.location.href = href;
          }
        })
        .catch(() => {
          window.location.href = href;
        });
    });
  });

});
