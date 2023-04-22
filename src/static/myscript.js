function myFunction() {
  let text;
  if (confirm("Do you want to continue?\nChoose Ok/Cancel") == true) {
    text = "You pressed OK!";
  } else {
    text = "You pressed cancel";
  }

  document.getElementById("response").innerHTML = text;
}
