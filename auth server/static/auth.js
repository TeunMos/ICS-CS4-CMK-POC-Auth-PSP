async function login(event) {
    event.preventDefault(); // prevent form from submitting

    console.log("login function called");
  
    const formData = new FormData(event.target); // get form data

    const redirect_url = formData.get('redirect_url');
   
    // send username and password to server using form data
    const response = await fetch(`/login`, {
        method: 'POST',
        body: formData
    });
    
    const code = response.status; // get response code

    if (code == 200) {
        console.log("login successful");


        // get body of response
        const body = await response.json();

        console.log(body);
    }
    else if (code == 401) {
        alert("Incorrect username or password");
    }
    else {
        alert("Error");
    }

  }