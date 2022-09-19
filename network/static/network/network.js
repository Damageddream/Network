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
            document.getElementById(`button_${post.id}`).onclick = () => {
                document.querySelector(`#post_${post.id}`).style.display='none';
                document.querySelector(`#edit_${post.id}`).style.display='block';
                console.log(`#edit-post-${post.id}`)         
            }
            document.querySelector(`#edit-post-${post.id}`).onsubmit = () => {
                console.log("submit")
                fetch(`editp/${post.id}`, {
                    method: "POST",
                    body: JSON.stringify({
                        text: document.querySelector(`#text_${post.id}`).value
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })
                
            }

            

        })
    })

}