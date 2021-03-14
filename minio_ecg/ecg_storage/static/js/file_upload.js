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

function arrayBufferToWordArray(ab) {
    var i8a = new Uint8Array(ab);
    var a = [];
    for (var i = 0; i < i8a.length; i += 4) {
        a.push(i8a[i] << 24 | i8a[i + 1] << 16 | i8a[i + 2] << 8 | i8a[i + 3]);
    }
    return CryptoJS.lib.WordArray.create(a, i8a.length);
}

function getSha1CryptoJS(inputArrayBuffer) {
    //преобразование к формату CryptoJS
    const inputWordArray = arrayBufferToWordArray(inputArrayBuffer);
    //получение хеша
    const hash = CryptoJS.SHA1(inputWordArray);
    return hash;
}

async function getHash_crypto(inputArrayBuffer, hashAlgorithm) {
    //вычисление хеша встроенной функцией браузера
    const result = await crypto.subtle.digest(hashAlgorithm, inputArrayBuffer);
    //преобразование к строке
    const stringHash = Array.prototype.map.call(new Uint8Array(result), x => (('00' + x.toString(16)).slice(-2))).join('');
    return stringHash;
}

async function getSha1FromFile(inputFile) {
    var reader = new FileReader();
    //назначение действия после полного чтения файла
    reader.onload = (function () {
        return async function (e) {
            //использовать CryptoJS если crypto.subtle не поддерживается
            if (crypto.subtle == undefined) {
                //создание хеша средствами сторонней библиотеки
                file_hash.value = getSha1CryptoJS(e.target.result);
            }
            else {
                //создание хеша средствами браузера может не поддерживаться в старых браузерах(или если соединение не https)
                file_hash.value = await getHash_crypto(e.target.result, 'SHA-1');
            }
        };
    })();
    //чтение файла
    reader.readAsArrayBuffer(inputFile);
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
    await getSha1FromFile(fileInput.files[0]);
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