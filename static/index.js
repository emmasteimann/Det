document.addEventListener("DOMContentLoaded", function(){

    let passForm = document.getElementById("passIn")
    let passField = document.getElementById("chatroomPass")
    let isPublic = document.getElementById("exampleCheck1")
    isPublic.addEventListener("click",()=>{
        passField.value=""
        passForm.classList.toggle("noPass");
    })

})