var ecg_id = document.getElementById('id_ecg_id_field');
var sample_frequency = document.getElementById('id_sample_frequency_field');
var amplitude_resolution = document.getElementById('id_amplitude_resolution_field');
var fileInput = document.getElementById('id_ecg_file_select');
var file_hash = document.getElementById('id_file_hash');
var file_format = document.getElementById('id_file_format');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//список полей и предназначенных для них списков ошибок
let field_to_error_list = new Map();
field_to_error_list.set('ecg_id_field', 'ecg_id_error_list');
field_to_error_list.set('sample_frequency_field', 'sample_frequency_error_list');
field_to_error_list.set('amplitude_resolution_field', 'amplitude_resolution_error_list');
field_to_error_list.set('file_hash', 'ecg_file_error_list');
field_to_error_list.set('file_format', 'ecg_file_error_list');

//если crypto.subtle по той или иной причине не поддерживается подключить CryptoJS
if (crypto.subtle == undefined) {
    var CryptoJS_script = document.createElement('script');
    CryptoJS_script.type = 'text/javascript';
    //необходимо подключить только необходимые модули долгая загрузка https://cdnjs.com/libraries/crypto-js
    CryptoJS_script.src = "https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js";
    //CryptoJS_script.integrity="sha512-nOQuvD9nKirvxDdvQ9OMqe2dgapbPB7vYAMrzJihw5m+aNcf0dX53m6YxM4LgA9u8e9eg9QX+/+mPu8kCNpV2A==";
    //CryptoJS_script.crossorigin="anonymous";
    document.head.appendChild(CryptoJS_script);
}

function arrayBufferToWordArray(ab) {
    var i8a = new Uint8Array(ab);
    var a = [];
    for (var i = 0; i < i8a.length; i += 4) {
        a.push(i8a[i] << 24 | i8a[i + 1] << 16 | i8a[i + 2] << 8 | i8a[i + 3]);
    }
    return CryptoJS.lib.WordArray.create(a, i8a.length);
}

function CryptoJS_Get_Sha1_FromFile(inputFile) {
    var reader = new FileReader();
    reader.onload = (function () {
        return async function (e) {
            const arrayBuffer = e.target.result;
            const hash = CryptoJS.SHA1(arrayBufferToWordArray(arrayBuffer));
            //преобразование ArrayBuffer к строке
            file_hash.value = hash;
        };
    })();
    //чтение файла
    reader.readAsArrayBuffer(inputFile);
}

async function getFileHash_crypto(inputFile, hashAlgorithm) {
    var reader = new FileReader();
    //назначение действия после полного чтения файла
    reader.onload = (function () {
        return async function (e) {
            //создание хеша средствами браузера может не поддерживаться в старых браузерах(или если соединение не https)
            let result = await crypto.subtle.digest(hashAlgorithm, e.target.result);
            //преобразование ArrayBuffer к строке
            file_hash.value = Array.prototype.map.call(new Uint8Array(result), x => (('00' + x.toString(16)).slice(-2))).join('');
        };
    })();
    //чтение файла
    reader.readAsArrayBuffer(inputFile);
}

async function getSHA_1FromFile(inputFile) {
    //использовать CryptoJS если crypto.subtle не поддерживается
    if (crypto.subtle == undefined) {
        await CryptoJS_Get_Sha1_FromFile(inputFile);
    } else {
        await getFileHash_crypto(inputFile, 'SHA-1');
    }
}

fileInput.addEventListener("change", async function (evt) {
    //разделение имени файла на несколько подстрок для получения расширения файла
    const splitFileName = fileInput.files[0].name.split('.');
    //добавить вывод ошибки если файл не имеет расширения
    if (splitFileName.length < 2) {
        return;
    }
    file_format.value = splitFileName[splitFileName.length - 1];
    //получение хеша файла
    await getSHA_1FromFile(fileInput.files[0]);
});

document.getElementById('ecg_upload_form').addEventListener("submit", async function (evt) {
    //запрет стандартного действия после нажатия sumbit
    evt.preventDefault();

    //формирование post запроса
    var formData = new FormData();
    formData.append('ecg_id_field', ecg_id.value);
    formData.append('sample_frequency_field', sample_frequency.value);
    formData.append('amplitude_resolution_field', amplitude_resolution.value);
    formData.append('file_format', file_format.value);
    formData.append('file_hash', file_hash.value);

    axios({
        method: "post",
        url: document.URL,
        data: formData,
        headers: { "Content-Type": "multipart/form-data", "X-CSRFToken": csrftoken },
    })
        .then(function (response) {
            //handle success
            console.log(response);
        })
        .catch(function (response) {
            //handle error
            //console.log(response.response);
            //удаление текущих ошибок
            const lists = document.querySelectorAll('.errorlist');
            for (const list of lists) {
                while (list.firstChild) {
                    list.removeChild(list.firstChild);
                }
            }
            //список ошибок
            var error_response = response.response.data;
            //заполнение ошибок
            for (let [field_name, list_name] of field_to_error_list) {
                if (error_response[field_name] != undefined) {
                    let error_list = document.getElementById(list_name);
                    error_response[field_name].forEach(function (item, i, arr) {
                        let li_ = document.createElement('li');
                        li_.innerHTML = item;
                        error_list.appendChild(li_);
                    });
                }
            }
        });
});