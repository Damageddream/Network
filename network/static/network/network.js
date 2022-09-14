document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.edit-b').addEventListener('click', () => {
        edit()
    })


    document.querySelector('.edit').style.display='none';
    document.querySelector('.post').style.display='block';
  });

function edit() {
    document.querySelector('.edit').style.display='block';
    document.querySelector('.post').style.display='none';

}