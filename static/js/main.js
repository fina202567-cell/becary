// ダミー決済アニメーション
function payNow(){
 let box=document.getElementById('paymentBox');
 box.innerHTML='Processing Payment...';
 setTimeout(()=>{
   box.innerHTML='✅ Payment Successful!';
 },2000);
}
