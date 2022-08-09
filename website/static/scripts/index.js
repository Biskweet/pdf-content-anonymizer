var lang = "en"

function triggerFileInput(elem) {
    let submitButton = document.querySelector("#hidden input");

    if (elem.files.length == 0) return;

    let totalSize = 0;
    for (file of elem.files) {
        totalSize += file.size;
    }

    if ((elem.files.length == 1 && elem.files[0].name.slice(-4).toUpperCase() == ".PDF") || (elem.files.length > 1 && totalSize < 32 * 1024 * 1024)) {
        if (elem.files.length == 1) {
            document.querySelector("#uploadValidator").innerHTML = `${elem.files[0].name} (${formatBytes(totalSize)})`;
        } else {
            document.querySelector("#uploadValidator").innerHTML = elem.files.length + ((lang == "en") ? " files selected" : "fichiers sélectionnés") + ` (${formatBytes(totalSize)})`;
        }

        submitButton.disabled = false;
        submitButton.style.backgroundColor = "#710d02";  // Base red
        submitButton.style.color = "#f6f2f2";            // Base pink
        submitButton.style.cursor = "pointer";
    } else {
        if (totalSize > 32 * 1024 * 1024) {
            document.querySelector("#uploadValidator").innerHTML = (lang == 'en') ? `Total size (${formatBytes(totalSize)}) must be lower than 32 MB` : `La taille totale (${formatBytes(totalSize)}) doit être sous 32 Mo`;
        } else {
            document.querySelector("#uploadValidator").innerHTML = (lang == 'en') ? "File type isn't PDF!" : "Le fichier doit être de type PDF !";
        }
        submitButton.disabled = true;
        submitButton.style.backgroundColor = "#b28a85";  // Greyed red
        submitButton.style.color = "#d3b5b5";            // Greyed pink
        submitButton.style.cursor = "default";
    }

    setTimeout(() => {
        document.querySelector("#hidden").style.display = "inline";
    }, 300);
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + sizes[i];
}


function showLoadingAnimation(elem) {
    let submitButton = document.querySelector("#hidden input");
    let loadingAnimation = document.querySelector("#loadingAnimation");

    submitButton.style.display = "none";

    loadingAnimation.style.display = "inline";
}


function changeLanguage(language) {
    lang = language;

    if (lang == "fr") {
        document.querySelector("label#fileinput_single_label").innerHTML = "Téléverser un seul fichier";
        document.querySelector("label#fileinput_mult_label").innerHTML = "Téléverser plusieurs fichiers";
    } else {
        document.querySelector("label#fileinput_single_label").innerHTML = "Upload a single file";
        document.querySelector("label#fileinput_mult_label").innerHTML = "Upload multiple files";
    }

    // In case the upload validator has an error
    type_err_p = document.querySelector("#uploadValidator");
    if (["File type isn't PDF!", "Le fichier doit être de type PDF !"].includes(type_err_p.innerHTML))
        type_err_p.innerHTML = (lang == 'en') ? "File type isn't PDF!" : "Le fichier doit être de type PDF !";
}
