    // get search form and page links
    let searchForm = document.getElementById("search_from");
    let pageLinks = document.getElementsByClassName("page-link");
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const searchParam = urlParams.get('search_query');

    // ensure search form exists
    if (typeof searchForm !== 'undefined') {
        for (let i=0; pageLinks.length > i; i++) {
            pageLinks[i].addEventListener("click", function (e) {
            // the function this way doesn't work
//                e.preventDefault();
//
//                // get data attrib
//                let page = this.dataset.page;
//
//                // add hidden search input to form
//                console.log(searchForm);
//                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`;
//
//                // submit form
//                searchForm.submit();

            // so I changed the link
                    if (searchParam) {
                        this.href += "&search_query=" + searchParam;
                        //e.preventDefault();
                        //console.log(typeof this.href, this.href);
                    }
            }
            );
        }
    };