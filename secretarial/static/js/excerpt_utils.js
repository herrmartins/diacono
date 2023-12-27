const options = id_minute_excerpts.options;
const copy_btn = document.getElementById("copy_button");
const t_area = document.getElementById("excerpt_t_area");
let dataToPost;
let optionValue;

id_minute_excerpts.onchange = function (e) {
	e.preventDefault();

	optionValue = this.value;

	// Check if an option is selected
	if (!optionValue) {
		copy_btn.setAttribute("disabled", "disabled");
		copy_btn.className = "btn btn-secondary disabled";
		t_area.textContent = "";
	} else {
		copy_btn.removeAttribute("disabled");
		copy_btn.className = "btn btn-primary";

		fetch(`http://127.0.0.1:8000/api/${optionValue}`)
			.then((res) => res.json())
			.then((data) => {
				dataToPost = data;
				console.log(data);
				t_area.textContent = data.excerpt;
				console.log(`Antes do novo fetch: ${data}`);
			});
	}
};

copy_button.onclick = (e) => {
	e.preventDefault();

	t_area.select();
	try {
		// Execute the copy command to copy the selected text to the clipboard
		document.execCommand("copy");
	} catch (err) {
		console.error("Unable to copy text: ", err);
	}
};
