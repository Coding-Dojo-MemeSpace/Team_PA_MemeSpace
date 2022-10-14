// Cat API
// API step 4 (create route to fetch api data) ->controllers file --
function getMemeData(){
    // We are creating a new route to go get(fetch) the data from the API site and bring it back so we can manipulate it
    //fetch = go get data at this url
    fetch('http://localhost:5000/meme_data')
            // the respose.json is coming from the controller route
            .then( response => response.json() )
            //     We now have an array of objects called data(JavaScript)
            .then( data => {
            // need to use the console in the inspect tool on the brower to see infomration 
            console.log(data)
        // we need a JavaScript for loop to go through the array of objects 
        // for (let i=0; i<data.length; i++){ //With this API, we do not have a array of objects so we dont need the loop
            // We want to create an image that we place in our "meme" div. 
            img = document.createElement("img")
            // data = array of ojbects,["url"]= key for key value pair
            img.setAttribute("src", data['url'])
        //     // We can set the height of the picture
            img.setAttribute("height", 250)
        //     //getElementById calls the ID name in the html.add image to html Id.
            document.getElementById("meme").append(img)
    })
    }
    getMemeData();
