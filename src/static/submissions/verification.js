window.addEventListener("load", function () {
  (function ($) {
    let codeblock = $("div.form-row.field-source_code div div.readonly");
    let codeblockValue = codeblock.html();
    console.log(codeblockValue);
    codeblockValue = codeblockValue.replaceAll('<br>', '\n');
    codeblock.html(`<pre><code>${codeblockValue}</code></pre>`)
    hljs.highlightAll();

    let snapshot = $("div.form-row.field-snapshot div div.readonly a");
    let snapshotUrl = snapshot.attr("href");
    snapshot.html(`<img src="${snapshotUrl}" alt="snapshot" class="responsive">`)
    console.log(snapshotUrl);

  })(django.jQuery);
});
