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

        const id_token = body.id_token;
        // redirect to redirect url with token
        window.location.href = `${redirect_url}?id_token=${id_token}`;

    }
    else if (code == 401) {
        alert("Incorrect username or password");
    }
    else {
        alert("Error");
    }

  }


async function register(event) {
    event.preventDefault(); // prevent form from submitting

    console.log("register function called");
  
    const formData = new FormData(event.target); // get form data

    console.log(formData.get('password'));

    // check if passwords match
    const password = formData.get('password');
    const password2 = formData.get('confirm_password');

    
    if (password != password2) {
        alert("Passwords do not match");
        return;
    }
   
    // send username and password to server using form data
    const response = await fetch(`/register`, {
        method: 'POST',
        body: formData
    });
    
    const code = response.status; // get response code

    if (code == 200) {
        console.log("registration successful");

        // get body of response
        const body = await response.json();

        console.log(body);

        alert("Registration successful");
    }
    else if (code == 409) {
        alert("Username already exists");
    }
    else {
        alert("Error");
    }

  }