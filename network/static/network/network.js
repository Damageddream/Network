document.addEventListener('DOMContentLoaded', function() {

    
    edit()


    document.querySelector('.edit').style.display='none';
    document.querySelector('.post').style.display='block';
  });

function edit() {
    fetch('/edit')
    .then(response => response.json())
    .then(posts =>{
        console.log(posts);
    })

}