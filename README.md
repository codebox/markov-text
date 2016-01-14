# markov-text
This is a Python implementation of a Markov Text Generator.

A [Markov Text Generator](http://en.wikipedia.org/wiki/Markov_chain) can be used to randomly generate (somewhat) realistic sentences, using words from a source text. Words are joined together in sequence, with each new word being selected based on how often it follows the previous word in the source document.

The results are often just nonsense, but at times can be strangely poetic - the sentences below were generated from the text of The Hitchhikers Guide to the Galaxy:

> Bits of perpetual unchangingness.  
> So long waves of matter, strained, twisted sharply.  
> So they are going to undulate across him and the species.  
> The barman reeled for every particle of Gold streaked through her eye.  
> We've met, haven't they? Look, said Ford never have good time you are merely a receipt.  
> The silence was delighted.

### Parsing

<section>To use the utility, first find a source document (the larger the better) and save it as a UTF-8 encoded text file. Executing the utility in 'parse' mode, as shown, will create a .db file containing information about how frequently words follow other words in the text file.

<pre>python markov.py parse &lt;name&gt; &lt;depth&gt; &lt;file&gt;
</pre>

*   The `name` argument can be any non-empty value - this is just the name you have chosen for the source document
*   The `depth` argument is a numeric value (minimum 2) which determines how many of the previous words are used to select the next word. Normally a depth of 2 is used, meaning that each word is selected based only on the previous one. The larger the depth value, the more similar the generated sentences will be to those appearing in the source text. Beyond a certain depth the generated sentences will be identical to those appearing in the source.
*   The `file` argument indicates the location of the source text file

For example:

<pre>python markov.py parse hitchhikers_guide 2 /path/to/hitchhikers.txt
</pre>

The parsing process may take a while to complete, depending on the size of the input document.</section>

### Generating

<section>To generate new sentences, run the utility in 'generate' mode, using the name specified during the parse operation

<pre>python markov.py gen &lt;name&gt; &lt;count&gt;
</pre>

*   The `name` argument should match the name used with the earlier `parse` command
*   The `count` argument is a numeric value indicating how many sentences to generate

For example:

<pre>>python markov.py gen hitchhikers_guide 3
Look, I can't speak Vogon! You don't need to touch the water
He frowned, then smiled, then tried to gauge the speed at which they were able to pick up hitch hikers
The hatchway sealed itself tight, and all the streets around it
</pre>

</section>
