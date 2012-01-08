# Script to manage La Grange version 2012

This script will take a very simple html file and will make it ready to be published to La Grange. The raw article contains only the blog post and no stylesheets, Web site titles, etc. The script process the raw file and prepare it for publishing adding the relevant link. 

The script must be able to reprocess an already publish file. I should not be dependent on keeping the raw version of each blog post. Once published I can work with the published version. 

## to implement List of things for processing the raw article

These are the elements I need to add to the final file before publishing it.

### UTF-8 only

The script is for the future but could be practical to process old files.

    if meta charset doesn't exist
        add <meta charset="utf-8">
    if meta charset exists
        is it utf-8?
            yes. exit
        is it another CHARSET?
            Tell it
            (OPTIONS)
            convert to utf-8
            replace by <meta charset="utf-8"> if doctype html5
            replace by the appropriate meta for the doctype

### Add the `head` element

    if STATUS=="draft"
    then add <head>…<head>

### Mobile ready unfortunately

As long as the `@viewport` rule for viewport is not ready and implemented in other browser we can't use it. `@o-viewport` only Opera for now.

    if STATUS=="draft"
    then <meta name="viewport" content="width=device-width">

### Add the blog title to the title

    if STATUS=="draft"
    then <title>posttitle + " - " + SITENAME</title>

### Add the stylesheet STYLESHEET

The stylesheet must be locally changeable to allow specific temp style for a trip or something.

    if STATUS=="draft"
    then <link rel="stylesheet" href="STYLESHEET"/>

### Add the name to the Web site

    if STATUS=="draft"
    <a rel="home" class="nomSite" href="http://DOMAIN/">SITENAME</a>

TODO Check the values for rel for home page 
    
### Add the link to the archives

    if STATUS=="draft"
    <a rel="archive" class="archives" href="/map" title="Archives">Ⓐ</a>

TODO Check the values for rel for archives page

### header format

NOT STABLE

    <header>
        <div class="meta pubdates">
            <span class="pubdate">
                <span class="pubdate-msg">Publié : </span>
                <span class="longdate">8 décembre 2011</span>
            </span>
            <span class="maj">
                <span class="maj-msg">Mise à jour : </span>
                <span class="isodate">2011-12-09</span>
            </span>
        </div>
    <h1>Un nouveau design ajusté pour La Grange 
        <span lang="ja">森野</span>　</h1>
    </header>

In the raw blog post

    <h1>Un nouveau design ajusté pour La Grange 
        <span lang="ja">森野</span></h1>
    <p class="datepub">2012-01-08</p>
    <p class="dateupd">2012-01-09</p>

### footer format

NOT STABLE.

Need to add the footer.

    <footer> 
    <address id="signature">Ce texte est publié par 
    <span id="auteur"><a href="/karl/">Karl</a></span> 
    sous un <a rel="license" 
    href="http://creativecommons.org/licenses/by/2.0/fr/">contrat 
    Creative Commons</a>. 
    <a id="glicense" rel="license" 
    href="http://creativecommons.org/licenses/by/2.0/fr/">
    <img alt="Creative Commons License" 
    style="padding:0 1em;margin-bottom:7px;border-width:0" 
    src="/2011/09/30/style/80x15-by" /></a></address>
    </footer>

### Article wrapping

NOT STABLE. Surely needs a bit of work

    <article>
        <header>
            Publication dates
            <h1>title</h1>
        </header>
        content.
    </article>
    <footer>
        Who and licenses
    </footer>

