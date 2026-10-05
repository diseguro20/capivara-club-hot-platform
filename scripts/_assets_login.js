(() => {
 const byId=id=>document.getElementById(id);let email='',temporary='';
 async function post(url,data){const r=await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const body=await r.json();if(!r.ok)throw new Error(body.error||'Não foi possível concluir.');return body;}
 async function submit(form,action){const button=form.querySelector('button[type=submit]');button.disabled=true;try{await action();}catch(e){ClubUI.alert(e.message);}finally{button.disabled=false;}}
 byId('loginForm').addEventListener('submit',e=>{e.preventDefault();submit(e.target,async()=>{
  email=byId('email').value.trim();temporary=byId('password').value;
  const result=await post('/api/login',{email,password:temporary});
  if(result.mustChangePassword){byId('loginScreen').classList.add('hidden');byId('forcePasswordScreen').classList.remove('hidden');}
  else location.reload();
 });});
 byId('forcePasswordForm').addEventListener('submit',e=>{e.preventDefault();submit(e.target,async()=>{
  const password=byId('newPassword').value;if(password!==byId('newPasswordConfirm').value)throw new Error('As senhas não coincidem.');
  await post('/api/set-initial-password',{email,currentPassword:temporary,newPassword:password});temporary='';location.reload();
 });});
 const modal=byId('resendModal');const close=()=>{modal.classList.add('hidden');modal.setAttribute('aria-hidden','true');};
 byId('resendPassword').addEventListener('click',()=>{modal.classList.remove('hidden');modal.setAttribute('aria-hidden','false');byId('resendEmail').value=byId('email').value;byId('resendEmail').focus();});
 byId('resendModalClose').addEventListener('click',close);modal.addEventListener('click',e=>{if(e.target===modal)close();});document.addEventListener('keydown',e=>{if(e.key==='Escape')close();});
 byId('resendSubmit').addEventListener('click',async()=>{const button=byId('resendSubmit');const input=byId('resendEmail');if(!input.reportValidity())return;button.disabled=true;try{await post('/api/resend-password',{email:input.value.trim()});ClubUI.alert('Se o e-mail tiver acesso ativo, você receberá o link para definir sua senha.');close();}catch(e){ClubUI.alert(e.message);}finally{button.disabled=false;}});
})();
