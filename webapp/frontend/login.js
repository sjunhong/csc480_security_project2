function login() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const xhttp = new XMLHttpRequest();
  const url = 'http://f6b4-163-120-30-85.eu.ngrok.io';
  xhttp.open('POST', `${url}/auth/signin`);
  let formData = new FormData();
  formData.append('id', username);
  formData.append('pw', password);
  xhttp.send(formData);

  xhttp.onreadystatechange = function () {
    console.log(this.readyState);
    if (this.readyState == 4) {
      const objects = JSON.parse(this.responseText);
      console.log(objects);

      if (this.status == '200') {
        alert(objects.msg);
      } else {
        alert(objects.msg);
      }
    }
  };
  return false;
}
