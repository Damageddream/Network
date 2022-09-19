document.addEventListener('DOMContentLoaded', function() {
 
    edit()

;
  });

function edit() {
    
    fetch('/edit')
    .then(response => response.json())
    .then(posts =>{
        console.log(posts);
        posts.forEach((post) => {
            console.log(post);
            document.getElementById(`button_${post.id}`).onclick = () =>
            fetch(`edit/${post.id}`)
            .then(response => response.json())
            .then(t_post => {
                console.log(t_post)
            })
            
        })
    })

}