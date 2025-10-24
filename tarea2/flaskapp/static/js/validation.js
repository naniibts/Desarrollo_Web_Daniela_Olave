const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 3 && name.trim().length <= 200;
  
  return lengthValid;
}

const validateSector = (sector) => {
  if(!sector || sector.trim() === "") return true;
  let lengthValid = sector.trim().length <= 100;

  return lengthValid;
}

const validateContact = (contact) => {
  if(!contact) return false;
  let lengthValid = contact.trim().length >= 4 && contact.trim().length <= 50;  
    
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length <= 100;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 13;

  // validación de formato
  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validateFiles = () => {
  const contenedor = document.getElementById("contenedorFotos");
  const fileInputs = document.querySelectorAll("#contenedorFotos input[type='file']");
  let contador = 0

  for (const input of fileInputs) {
    if (input.files && input.files.length > 0)
      for (const file of input.files) {
          contador += 1
      
          // el tipo de archivo debe ser "image/<foo>" 
          if (!file.type.startsWith("image/")) {
              return false;
          }
      }
  }
  return contador >= 1 && contador <= 5;
};

const validateCant = (cant) => {
    return cant && parseInt(cant) >= 1;
}

const validateAge = (age) => {
    return age && parseInt(age) >= 1;
}

const validateType = (type) => {
    return type && type.trim() !== "";
}

const validateDescription = (description) => {
    if (!description) return false;
    const len = description.trim().length;
    return len >= 10 && len <= 500;
}

const validateDate = (date) => {
    if (!date) return false;

    const fechaSeleccionada = new Date(date);
    const inputFecha = document.getElementById("fecha");
    const fechaMinima = new Date(inputFecha.min); // Obtener la fecha mínima del atributo 'min'

    //validar que la fecha seleccionada sea válida (no 'Invalid Date') y sea >= a la mínima
    return !isNaN(fechaSeleccionada) && fechaSeleccionada >= fechaMinima;
};


const validateSelect = (select) => {
  if(!select) return false;
  return true
}

// Función para establecer la fecha mínima y el valor inicial
function setFechaEntrega() {
    const input = document.getElementById("fecha");
    if (!input) return; // Prevenir errores si el elemento no existe

    const ahora = new Date();
    const fechaMinima = new Date(ahora.getTime() + 3 * 60 * 60 * 1000); // Sumar 3 horas en milisegundos

    // Formatear la fecha al formato 'YYYY-MM-DDTHH:MM' requerido por datetime-local
    const año = fechaMinima.getFullYear();
    const mes = String(fechaMinima.getMonth() + 1).padStart(2, '0');
    const dia = String(fechaMinima.getDate()).padStart(2, '0');
    const horas = String(fechaMinima.getHours()).padStart(2, '0');
    const minutos = String(fechaMinima.getMinutes()).padStart(2, '0');

    const fechaFormateada = `${año}-${mes}-${dia}T${horas}:${minutos}`;

    // Establecer el valor mínimo y el valor actual del input
    input.min = fechaFormateada;
    input.value = fechaFormateada;
}

// Ejecutar la función cuando el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    setFechaEntrega();
});

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["myForm"];
  let region = myForm["select-region"].value;
  let comuna = myForm["select-comuna"].value;
  let sector = myForm["sector"].value;

  let name = myForm["nombre"].value;
  let email = myForm["email"].value;
  let phoneNumber = myForm["phone"].value;
  let socialMedia = myForm["select-red"].value; 
  let contact = myForm["red-id"].value;
  
  let type = myForm["select-tipo"].value;
  let cant = myForm["cantidad"].value;
  let age = myForm["edad"].value;
  let medida = myForm["select-medida"].value;
  let date = myForm["fecha"].value;
  let description = myForm["descripcion"].value;
    
  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }
  if (socialMedia !== "" && !validateSelect(socialMedia)) { 
    setInvalidInput("Red de Contacto");
  }

  if (socialMedia && !contact) {
    setInvalidInput("ID o URL de Contacto");
  } else if (socialMedia && !validateContact(contact)) {
    setInvalidInput("ID o URL de Contacto");
  }

  if (!validateName(name)) {
    setInvalidInput("Nombre");
  }
  if (sector && !validateSector(sector)) {
    setInvalidInput("Sector");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (phoneNumber && !validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número");
  }
  if(!validateDate(date)){
    setInvalidInput("Fecha");
  }
  if(!validateType(type)){
    setInvalidInput("Tipo de Mascota");
  }
  if (!validateCant(cant)) {
    setInvalidInput("Cantidad");
  }
  if (!validateAge(age)) {
    setInvalidInput("Edad");
  }

  if (!validateSelect(medida)) {
    setInvalidInput("Unidad de Medida");
 }

  if (description && !validateDescription(description)) {
    setInvalidInput("Descripción");
  }


  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });

  } else {
    myForm.style.display = "none";

    //mensaje de confirmación
    validationMessageElem.innerText = "¿Está seguro que desea agregar este aviso de adopción?";
    validationListElem.textContent = "";

    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    //botón "Sí, estoy seguro"
    let submitButton = document.createElement("button");
    submitButton.innerText = "Sí, estoy seguro";
    submitButton.style.marginRight = "10px";
    submitButton.className = "submit-button";
    submitButton.addEventListener("click", () => {
        formContainer.innerHTML = `
            <div style="text-align: center; padding: 40px;">
                <h2>Hemos recibido la información de adopción, muchas gracias y suerte!</h2>
                <button id="btnVolverPortada" style="margin-top: 20px; padding: 10px 20px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                    Volver a la portada
                </button>
            </div>
        `;

        //listener 
        document.getElementById("btnVolverPortada").addEventListener("click", () => {
            window.location.href = "portada.html"; // Asume que tu portada se llama index.html
        });
    });

    //botón "No, no estoy seguro..."
    let backButton = document.createElement("button");
    backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
    backButton.className = "back-button";
    backButton.addEventListener("click", () => {
        myForm.style.display = "block";
        validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    validationBox.hidden = false;
  }
};

//listener para el botón agregar fotos
document.getElementById("agregarFoto").addEventListener("click", () => {
    const contenedor = document.getElementById("contenedorFotos");
    const fileInputs = contenedor.querySelectorAll("input[type='file']");

    //verificar que no haya más de 5 inputs
    if (fileInputs.length >= 5) {
        return;
    }
    //crear el input
    const nuevoInput = document.createElement("input");
    nuevoInput.type = "file";
    nuevoInput.name = "fotos[]";
    nuevoInput.accept = "image/*";
    nuevoInput.required = false;

    contenedor.appendChild(nuevoInput);
});

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);
