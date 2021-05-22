var ecg_id = document.getElementById('id_ecg_id_field'); //переменная поля экг id
var sample_frequency = document.getElementById('id_sample_frequency_field'); //переменная поля Sample frequency
var amplitude_resolution = document.getElementById('id_amplitude_resolution_field'); //переменная Amplitude resolution
var fileInput = document.getElementById('id_ecg_file_select'); //поле выбора файла
var file_hash = document.getElementById('id_file_hash'); //скрытое поле для хеша файла
var file_format = document.getElementById('id_file_format'); //скрытое поле для расширения файла
var original_file_name = document.getElementById('id_original_file_name'); //скрытое поле для имени файла
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value; //токен для отправки данных на сервер

let field_to_error_list = new Map(); //список полей и предназначенных для них списков ошибок
field_to_error_list.set('ecg_id_field', 'ecg_id_error_list');
field_to_error_list.set('sample_frequency_field', 'sample_frequency_error_list');
field_to_error_list.set('amplitude_resolution_field', 'amplitude_resolution_error_list');
field_to_error_list.set('file_hash', 'ecg_file_error_list');
field_to_error_list.set('file_format', 'ecg_file_error_list');
field_to_error_list.set('original_file_name', 'ecg_file_error_list');

//очистка списка ошибок
function error_list_clean() {
    const lists = document.querySelectorAll('.errorlist');
    for (const list of lists) {
        while (list.firstChild) {
            list.removeChild(list.firstChild);
        }
    }
}

//функция преобразования arrayBuffer к формату CryptoJS WordArray
function arrayBufferToWordArray(ab) {
    var i8a = new Uint8Array(ab);
    var a = [];
    for (var i = 0; i < i8a.length; i += 4) {
        a.push(i8a[i] << 24 | i8a[i + 1] << 16 | i8a[i + 2] << 8 | i8a[i + 3]);
    }
    return CryptoJS.lib.WordArray.create(a, i8a.length);
}
//получение хеша из ArrayBuffer с помощью CryptoJS
function getSha1CryptoJS(inputArrayBuffer) {
    //преобразование к формату CryptoJS
    const inputWordArray = arrayBufferToWordArray(inputArrayBuffer);
    //получение хеша
    const hash = CryptoJS.SHA1(inputWordArray);
    return hash;
}
//получение хеша из ArrayBuffer средствами браузера
async function getHash_crypto(inputArrayBuffer, hashAlgorithm) {
    //вычисление хеша встроенной функцией браузера
    const result = await crypto.subtle.digest(hashAlgorithm, inputArrayBuffer);
    //преобразование к строке
    const stringHash = Array.prototype.map.call(new Uint8Array(result), x => (('00' + x.toString(16)).slice(-2))).join('');
    return stringHash;
}
//получение хеша указанного файла
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
//при каждом выборе другого файла
fileInput.addEventListener("change", async function (evt) {
    //имя файла
    original_file_name.value = fileInput.files[0].name;
    //разделение имени файла на несколько подстрок для получения расширения файла
    const splitFileName = fileInput.files[0].name.split('.');
    //пустое значение если файл не имеет расширения(для дальнейшей проверки)
    if (splitFileName.length < 2) {
        file_format.value = '';
        return;
    }
    else {
        file_format.value = splitFileName[splitFileName.length - 1];
    }
    //получение хеша файла
    await getSha1FromFile(fileInput.files[0]);
});

//событие при нажатии кнопки отправки формы
document.getElementById('ecg_upload_form').addEventListener("submit", async function (evt) {
    //запрет стандартного действия после нажатия sumbit
    evt.preventDefault();
    //удаление текущих ошибок
    error_list_clean();

    if (file_format.value.length < 1) {
        let error_list = document.getElementById(field_to_error_list.get('file_format'));
        let li_ = document.createElement('li');
        li_.innerHTML = "Ошибка получения расширения файла(возможно файл не имеет расширения)";
        error_list.appendChild(li_);
        return;
    }

    if (file_hash.value.length != 40) {
        let error_list = document.getElementById(field_to_error_list.get('file_hash'));
        let li_ = document.createElement('li');
        li_.innerHTML = "Ошибка рассчёта хеша файла";
        error_list.appendChild(li_);
        return;
    }

    //формирование post запроса
    var formData = new FormData();
    formData.append('ecg_id_field', ecg_id.value);
    formData.append('sample_frequency_field', sample_frequency.value);
    formData.append('amplitude_resolution_field', amplitude_resolution.value);
    formData.append('file_format', file_format.value);
    formData.append('file_hash', file_hash.value);
    formData.append('original_file_name', original_file_name.value);

    //отправка данных на сервер
    axios({
        method: "post",
        url: api_upload_url,
        data: formData,
        headers: { "Content-Type": "multipart/form-data", "X-CSRFToken": csrftoken },
    })
        .then(function (response) {
            //Если сервер вернул что в данных нет ошибки
            //console.log(response);
            const input_data = response.data; //json с данными
            //отправка файла в minio
            axios({
                method: "put",
                url: input_data['upload_url'],
                data: fileInput.files[0],
            })
                .then(function (response) {
                    //перенаправить на указанный адрес при успешной загрузке
                    document.location.href = input_data['redirect_url'];
                })
                .catch(function (response) {
                    //предполагается сделать запрос на удаление записи о файле на сервере если он не был загружен в minio(для этого передаётся ecg_file_id в json)
                    console.log(response.response);
                })
        })
        .catch(function (response) {
            //handle error
            //console.log(response.response);
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