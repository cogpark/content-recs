document.addEventListener("DOMContentLoaded", async () => { 
    const form = document.getElementById('submit-url');
    form.addEventListener('click', async(event) => {
        event.preventDefault();
        let url = document.getElementById('user-url').value;
        console.log(url);
        let data = await getRecs(url);
        updateAssessment(data)
    }
)})

async function getRecs(url) {
    let response = await fetch(`/api/content-recs/${url}`)
    let data = response.json();
    return data 
}

function updateAssessment(data){
    console.log(data)
    const putDataHere = document.getElementById('title-assessment')
    putDataHere.innerHTML = ''

    let pageTitle = document.createElement("P");
    pageTitle.innerHTML = `<span>Page title: ${data['title']}<span/></span><br/><br/>`

    // TODO: if titleLength is fine, then don't say anything
    let titleLength = document.createElement("P");
    titleLength.innerHTML = `<span>Title length: ${data['title_length']['length']} characters. ${data['title_length']['assessment']}</span><br/>`

    let titleMatches = document.createElement("P");
    titleMatches.innerHTML = `<span>Found ${data['title_matches']['total']} pages with similar names. ${data['title_matches']['assessment']}</span><br/>`

    putDataHere.appendChild(pageTitle)
    putDataHere.appendChild(document.createElement('HR'))
    putDataHere.appendChild(titleLength)
    putDataHere.appendChild(document.createElement('HR'))
    
    if (data['acronym_checker']['acronym_checker'] > 0) {
        let acronym = document.createElement("P");
        acronym.innerHTML =  `<span>${data['acronym_checker']['assessment']}</span><br/>`
        putDataHere.appendChild(acronym)
        putDataHere.appendChild(document.createElement('HR'))
    }

    putDataHere.appendChild(titleMatches)

    if (data['title_matches']['total'] > 0) {
        let similar_titles_list = document.createElement('UL');
        putDataHere.appendChild(similar_titles_list)
        for (var key in data['title_matches']['title_matches']) {
            let similar_title = document.createElement("LI");
            similar_title.innerHTML = key
            similar_titles_list.appendChild(similar_title)           
        }
    }
    putDataHere.appendChild(document.createElement('HR'))

    if (data['trouble_words']['score'] > 0 ) {
        let trouble_words = document.createElement('P');
    }


}