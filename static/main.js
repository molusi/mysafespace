

const msg= document.querySelector(".alert");
const info = document.querySelector(".info")

window.addEventListener("DOMContentLoaded",()=>{
if(msg.contains(info)){
setTimeout(()=>msg.remove(),5000)}
});

const myForm = document.querySelector("#my-form")
const emailInput = document.querySelector("#email-input")
const passwordInput = document.querySelector("#password-input")
const mSg = document.querySelector("#mesg")


myForm.addEventListener('submit',onSubbmit);

function onSubmit(e){
  e.preventDefault();
  if(emailInput.value === '' || passwordInput.value ===''){
  mSg.classList.add('is-danger');
    mSg.innerHTML = "Please enter all fields";
    setTimeout(()=>msg.remove(),3000)
  }};


const control = document.querySelectorAll(".input");
const isDanger = document.querySelectorAll(".is-danger");



control.forEach((inpEl)=>{inpEl.addEventListener(('input'),isDanger.forEach((pr)=>setTimeout(()=>pr.remove(),4000)))})
