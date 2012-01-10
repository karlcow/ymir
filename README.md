# Script to manage La Grange version 2012

This script will take a very simple html file and will make it ready to be published to La Grange. The raw article contains only the blog post and no stylesheets, Web site titles, etc. The script process the raw file and prepare it for publishing adding the relevant link. 

The script must be able to reprocess an already publish file. I should not be dependent on keeping the raw version of each blog post. Once published I can work with the published version. 

## to implement List of things for processing the raw article

These are the elements I need to add to the final file before publishing it.

### DONE Check the status

    if document is status draft then DRAFT is True.
    <meta name="status" content="draft">
    
    getdocstatus(doc)

### TODO  extract the dates of the blog post

if STATUS == "draft"

    <meta name="created" content="2012-01-08">
    <meta name="modified" content="2012-01-08">

if STATUS == ["pub","acl"]

    <div class="meta pubdates">
        <span class="pubdate">
            <span class="pubdate-msg">Publié : </span>
            <span class="created longdate">1er décembre 2011</span>
        </span>
        <span class="maj">
            <span class="maj-msg">Mise à jour : </span>
            <span class="modified iso">2011-12-01</span>
        </span>
    </div>

TODO: to test if the date is in a good format

### TODO  UTF-8 only

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

### TODO Add the `head` element

    if STATUS=="draft"
    then add <head>…<head>

### TODO Mobile ready unfortunately

As long as the `@viewport` rule for viewport is not ready and implemented in other browser we can't use it. `@o-viewport` only Opera for now.

    if STATUS=="draft"
    then <meta name="viewport" content="width=device-width">

### TODO Add the blog title to the title

    if STATUS=="draft"
    then <title>posttitle + " - " + SITENAME</title>

### TODO Add the stylesheet STYLESHEET

The stylesheet must be locally changeable to allow specific temp style for a trip or something.

    if STATUS=="draft"
    then <link rel="stylesheet" href="STYLESHEET"/>

### TODO Add the name to the Web site

    if STATUS=="draft"
    <a rel="home" class="nomSite" href="http://DOMAIN/">SITENAME</a>

TODO Check the values for rel for home page 

### TODO Add the link to the archives

    if STATUS=="draft"
    <a rel="archive" class="archives" href="/map" title="Archives">Ⓐ</a>

[List of values for rel attributes](http://microformats.org/wiki/existing-rel-values#formats) that I might need.

* rel="copyright":  Refers to a copyright statement for the current document. (link, a)
* rel="license":  indicates that the [referenced document] is a license for the current page. (link, a)
* rel="start": Refers to the first document in a collection of documents. This link type tells search engines which document is considered by the author to be the starting point of the collection.
* rel="help": could be the way I would give access to a page giving more information about the relations. (to think about it)
* rel="home": indicates that the [referenced document] is the homepage of the site in which the current page appears. [proposal]
* rel="author": author of the current page, link to the author page (for me /karl/)
* rel="archive": index of archived entries
* rel="feed": the link is a feed

### TODO header format

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

#### title

    <h1>Un nouveau design ajusté pour La Grange 
        <span lang="ja">森野</span></h1>

#### date

See the date section

### TODO footer format

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

### TODO Article wrapping

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

### TODO add a logging system to know when things are wrong and where

See http://www.5dollarwhitebox.org/drupal/node/56

    import logging
 
    log = logging.getLogger()
    ch  = logging.StreamHandler()
 
    log.addHandler(ch)
 
    log.debug('this is a debug message')
    log.info('this is an informational message')
    log.warning('this is a warning message')
    log.error('this is an error message')
    log.critical('this is a critical message')