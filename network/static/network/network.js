document.addEventListener('DOMContentLoaded', function() {

        edit()
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
            document.getElementById(`like_${post.id}`).onclick = () => {
                fetch(`like/${post.id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                    })
                })
                .then(response => response.json())
                .then(post => {
                    console.log(post.likes)
                    document.querySelector(`#likes_${post.id}`).innerHTML= post.likes;
                })

                return false;

            }
            document.querySelector(`#edit-post-${post.id}`).onsubmit = () => {
                console.log("submit")
                fetch(`editp/${post.id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        text: document.querySelector(`#text_${post.id}`).value
                    })
                })
                .then(() => {
                    document.querySelector(`#post_${post.id}`).style.display='block';
                    document.querySelector(`#hid_${post.id}`).innerHTML= document.querySelector(`#text_${post.id}`).value;
                    document.querySelector(`#edit_${post.id}`).style.display='none';
                })

                return false;
                
            }

            

        })
    })

}