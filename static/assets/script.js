function hide_messages() {
  let messages = document.getElementById("messages");
  messages.style.display = "none";
}

function hidden_tag(tag) {
  tag.style.display = "none";
}

setTimeout(hide_messages, 30 * 1000);
