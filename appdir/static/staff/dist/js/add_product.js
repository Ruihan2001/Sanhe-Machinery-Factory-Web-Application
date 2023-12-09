$(document).on('click', '.delete', function() {
    console.log('ss')
     $(this).parent().parent().remove();
  })

$("#add-video").click(function () {
        console.log("clicked")
        let row = document.createElement('div')
        row.className = 'xl:flex items-center mt-5 first:mt-0'
        row.innerHTML = '                            <div class="input-group flex-1">\n' +
            '                                                                    <input type="text" class="form-control video_link"\n' +
            '                                                                           placeholder="Url Link">\n' +
            '                                                                </div>\n' +
            '                                                                <div class="w-20 flex text-slate-500 mt-3 xl:mt-0">\n' +
            '                                                                    <button class="ml-3 xl:ml-5 delete">\n' +
            '                                                                        <svg xmlns="http://www.w3.org/2000/svg"\n' +
            '                                                                             width="24" height="24" viewBox="0 0 24 24"\n' +
            '                                                                             fill="none" stroke="currentColor"\n' +
            '                                                                             stroke-width="2" stroke-linecap="round"\n' +
            '                                                                             stroke-linejoin="round" icon-name="trash-2"\n' +
            '                                                                             data-lucide="trash-2"\n' +
            '                                                                             class="lucide lucide-trash-2 w-4 h-4">\n' +
            '                                                                            <polyline points="3 6 5 6 21 6"></polyline>\n' +
            '                                                                            <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"></path>\n' +
            '                                                                            <line x1="10" y1="11" x2="10"\n' +
            '                                                                                  y2="17"></line>\n' +
            '                                                                            <line x1="14" y1="11" x2="14"\n' +
            '                                                                                  y2="17"></line>\n' +
            '                                                                        </svg>\n' +
            '                                                                    </button>\n' +
            '                                                                </div>'

        $("#video-link").append(row)
});
