(() => {
 let chain=Promise.resolve();
 function show(message,options={},confirmation=false){
  const open=()=>new Promise(resolve=>{
   const previous=document.activeElement;const dialog=document.createElement('dialog');dialog.className='club-dialog';
   dialog.innerHTML='<div class="club-dialog-content"><div class="club-dialog-brand">CAPIVARA CLUB HOT</div><h2 id="club-dialog-title"></h2><p id="club-dialog-message"></p><div class="club-dialog-actions"></div></div>';
   dialog.setAttribute('aria-labelledby','club-dialog-title');dialog.setAttribute('aria-describedby','club-dialog-message');
   dialog.querySelector('h2').textContent=options.title || (confirmation?'Confirmar ação':'Uma mensagem para você');dialog.querySelector('p').textContent=String(message);
   const finish=result=>{dialog.close();dialog.remove();previous?.focus();resolve(result);};
   const actions=dialog.querySelector('.club-dialog-actions');
   if(confirmation){const cancel=document.createElement('button');cancel.className='secondary';cancel.textContent='Cancelar';cancel.onclick=()=>finish(false);actions.append(cancel);}
   const ok=document.createElement('button');ok.textContent=options.confirmLabel || (confirmation?'Confirmar':'Entendi');ok.onclick=()=>finish(true);actions.append(ok);
   dialog.addEventListener('cancel',event=>{event.preventDefault();finish(false);});document.body.append(dialog);dialog.showModal();ok.focus();
  });
  const result=chain.then(open);chain=result.catch(()=>{});return result;
 }
 window.ClubUI={alert:(message,options)=>show(message,options),confirm:(message,options)=>show(message,options,true)};
 let invalidPending=false;
 document.addEventListener('invalid',event=>{event.preventDefault();if(invalidPending)return;invalidPending=true;const field=event.target;let message='Confira o valor informado.';if(field.validity.valueMissing)message='Preencha os campos obrigatórios para continuar.';else if(field.validity.typeMismatch)message='Informe um e-mail válido.';else if(field.validity.tooShort)message='O texto informado está muito curto.';ClubUI.alert(message,{title:'Confira os dados'}).then(()=>{invalidPending=false;field.focus();});},true);
})();
