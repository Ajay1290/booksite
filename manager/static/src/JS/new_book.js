var file_input = document.getElementById('file');

file_input.onchange = handleFileSelect;

function ValidateFile(){        
    if( file_input.files[0].type != "application/pdf") {
        alert('Error : Not a PDF');
        console.log('Error : Not a PDF');
        window.location.reload();
    }
};

function handelPDF(file){
    ValidateFile();
    document.getElementById('size').value = (file.size / (1024 * 1024)).toFixed(2).toString();
    var blob = new Blob([file], {type: "application/pdf"});
    var pdfBlob = URL.createObjectURL(blob);
    var loadingTask = pdfjsLib.getDocument(pdfBlob);        
    loadingTask.promise.then(function(pdf) {
        getPDFMetadata(pdf);
        pdf.getPage(1).then(function(page) {
            var scale = 1.5;
            var viewport = page.getViewport({ scale: scale, });

            var canvas = document.getElementById('the-canvas');
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext);
        });            
    });
}

function on_book_post(){
    document.getElementById('next_pg').click();
}
    

var progress = document.querySelector('.percent');
var reader = new FileReader();

// File Handler Function
function handleFileSelect(evt) {            
    var file = evt.target.files[0];
    reader.readAsBinaryString(file);
    handelPDF(file);    

    reader.onabort = function(e){
        alert('File read cancelled');
        console.log('File read cancelled');
        window.location.reload();
    };

    reader.onloadstart = function(e){document.getElementById('progress_bar').className = 'loading';};
    reader.onprogress = updateProgress;
    
    // Closure to capture the file information.
    reader.onload = function(theFile) {return function(e) {
            var progress = document.querySelector('.percent');                        
            progress.textContent = file.name
            getFileName(file)
        }(file);
    }        
}

// Cancle Button function
function abortRead() {
    reader.abort();
}


// Progress Bar Update function
function updateProgress(evt) {
    // evt is an ProgressEvent.
    if (evt.lengthComputable) {
        var percentLoaded = Math.round((evt.loaded / evt.total) * 100);
        console.log(percentLoaded)
        // Increase the progress bar length.        
        var progress = document.querySelector('.percent');
        progress.style.width = percentLoaded + '%';
        progress.textContent = percentLoaded + '%';        
    }
}

function getFileName(file){
    var title = document.getElementById('title');
    title.value = file.name;
}

function getPDFMetadata(pdf){
    document.getElementById('pages').value = pdf.numPages;
    pdf.getMetadata().then(function(data) {
        console.log(data["info"])
        console.log(data.metadata)
        let book_cr_prod = ["Microsoft® Word 2013", "mPDF 6.0", "Microsoft® Word 2010", "Adobe PDF Library 10.0.1", "Adobe PDF Library 9.0", undefined, "Acrobat Distiller 7.0.5 (Windows)", "www.it-ebooks.info", "3-Heights(TM) PDF Optimization Shell 4.8.25.2 (http://www.pdf-tools.com)", "calibre 0.9.13 [http://calibre-ebook.com]","Adobe Acrobat 8.1", "pdfTeX-1.40.17"]
        let book_cr_auth = ["www.it-ebooks.info", undefined]
        if(data.metadata){
            if(data.metadata._metadataMap.get("dc:language")){
                document.getElementById('language').value = data.metadata._metadataMap.get("dc:language")
            }
            if (data['info']['Title'] != undefined){title.value = data['info']['Title']}
            if(data['info']['Subject'] != undefined){title.value += " " + data['info']['Subject']}
            if(!book_cr_prod.includes(data.metadata._metadataMap.get("dc:publisher"))){
                document.getElementById('publisher').value = data.metadata._metadataMap.get("dc:publisher");
            }
            else if(!book_cr_prod.includes(data.metadata._metadataMap.get("pdf:producer"))){
                document.getElementById('publisher').value = data.metadata._metadataMap.get("pdf:producer");
            }
            if(data['info']['Custom']){
                if(data['info']['Custom']['EBX_PUBLISHER']){
                    document.getElementById('publisher').value = data['info']['Custom']['EBX_PUBLISHER'];
                }
                if(data['info']['Custom']['EBX_PUBLISHER']['name']){
                    document.getElementById('publisher').value = data['info']['Custom']['EBX_PUBLISHER']['name'];
                }
            }
            if(!book_cr_auth.includes(data.metadata._metadataMap.get("dc:creator"))){
                document.getElementById('authors').value = data.metadata._metadataMap.get("dc:creator");
            }
        }else{
            if(data['info']['Title'] != undefined){title.value = data['info']['Title']}
            if(data['info']['Subject'] != undefined){title.value += " " + data['info']['Subject']}
            if(data['info']['Custom']){
                if(data['info']['Custom']['EBX_PUBLISHER']){
                    document.getElementById('publisher').value = data['info']['Custom']['EBX_PUBLISHER'];}
            }
            else if(!book_cr_prod.includes(data['info']['Producer'])){
                document.getElementById('publisher').value = data['info']['Producer']
            }
            if (!book_cr_auth.includes(data['info']['Author'])){
                document.getElementById('authors').value = data['info']['Author']
            }
        }
    }).catch(function(err) {
        console.log('Error getting meta data');
        console.log(err);
    });
}

document.getElementById('upload-btn').onclick = () =>{
    document.getElementById('loader-wing').style.display = 'flex';
}