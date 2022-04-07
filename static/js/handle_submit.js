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
    url = url.replaceAll("/","|")
    console.log(url)
    let response = await fetch(`/api/content-recs/${url}`)
    let data = response.json();
    return data 
}

function updateAssessment(data){
    console.log(data)
    const putDataHere = document.getElementById('title-assessment')
    putDataHere.innerHTML = ''

    let pageTitle = document.createElement("P");
    pageTitle.innerHTML = `<span class="assessment-label">Your page's title:</span><span> ${data['title']}</span><hr/>`
    putDataHere.appendChild(pageTitle)

    // TODO: if titleLength is fine, then don't say anything
    let titleLength = document.createElement("P");
    titleLength.innerHTML = `<span class="assessment-label">Your title's length:</span><span> ${data['title_length']['length']} characters. ${data['title_length']['assessment']}</span><hr/>`
    putDataHere.appendChild(titleLength)
    

    let titleMatches = document.createElement("P");
    titleMatches.innerHTML = `<span class="assessment-label">Found ${data['title_matches']['total']} pages with similar names.</span><span> ${data['title_matches']['assessment']}</span>`
    putDataHere.appendChild(titleMatches)
    
    if (data['title_matches']['total'] > 0) {
        let similar_titles_list = document.createElement('UL');
        putDataHere.appendChild(similar_titles_list)
        for (var key in data['title_matches']['title_matches']) {
            console.log(key)
            let similar_title = document.createElement("LI");
            similar_title.innerHTML = "<a href='https://" + data['title_matches']['title_matches'][key] + "'>" + key + "</a>"
            similar_titles_list.appendChild(similar_title)           
        }
        putDataHere.appendChild(createElement('HR'))
    } else {
        putDataHere.appendChild(createElement('HR'))
    }

    if (data['acronym_checker']['acronym_checker'] > 0) {
        let acronym = document.createElement("P");
        acronym.innerHTML =  `<span>${data['acronym_checker']['assessment']}</span><hr/>`
        putDataHere.appendChild(acronym)
    }

    if (data['trouble_words']['score'] > 0 ) {
        let trouble_words = document.createElement('P');
        trouble_words.innerHTML = ''
    }


}

/*
(function() {
  var h, a, f;
  a = document.getElementsByTagName('link');
  for (h = 0; h < a.length; h++) {
    f = a[h];
    if (f.rel.toLowerCase().match(/stylesheet/) && f.href) {
      var g = f.href.replace(/(&|\?)rnd=\d+/, '');
      f.href = g + (g.match(/\?/) ? '&' : '?');
      f.href += 'rnd=' + (new Date().valueOf());
    }
  } // for
})() */