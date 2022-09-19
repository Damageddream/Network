document.addEventListener('DOMContentLoaded', function() {
 
    edit()

;
  });

function edit() {
    const h3 = document.querySelector("h3")
    const page = h3.id
    fetch(`/edit/${page}`)
    .then(response => response.json())
    .then((posts) =>{
        console.log(posts);
        posts.forEach((post) => {
            console.log(post);
            document.getElementById(`button_${post.id}`).onclick = () =>
            fetch(`edit/${post.id}`)
            .then(response => response.json())
            .then(t_post => {
                
            })
            
        })
    })

}