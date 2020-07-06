# -*- coding: utf-8 -*-
import fitz

def sorting_key(input):
	"""
        This function implements sort keys for the german language.

        :param input: input key
        :returns: output key
        """

	# key1: compare words lowercase and replace umlauts
	key1=input.casefold()
	key1=key1.replace(u"ä", u"a")
	key1=key1.replace(u"ö", u"o")
	key1=key1.replace(u"ü", u"u")
	key1=key1.replace(u"ß", u"ss")

	# key2: Ignore case when sorting
	key2=input.casefold()

	# in case two words are the same according to key1, sort the words
	# according to key2. 
	return (key1, key2)

def get_annotations(doc, sub):
    """
    Grabs annotations and page numbers from a pdf document.

    :param doc: path to pdf document
    :param sub: title/toc pages that are not to be counted as pages in the index
    :returns: list of raw annotation data
    """

    # The pdf document is read out in pages, so it grabs all annotations from
    # each page and adds them to one big list of tuples that contain the
    # annotation data as well as the page numbers where they are located
    doc = fitz.open(doc)
    annotations = []
    for page in doc:
        annot = page.firstAnnot
        # Add annotations to the list as long as there are any available on the
        # page
        while(annot != None):
            annotations.append((annot.info, page.number + 1 - sub))
            annot = annot.next

    return annotations

def process_annotations(annotations, sort):
    """
    Converts the raw annotation data to a format that Cindex can read.

    :param annotations: raw annotation data from get_annotations()
    :param sort: whether to sort the annotation list or not
    :returns: processed annotation data
    """

    # The format that the index entries are written is:
    # (entry text) [> page range]
    # page range is optional for the case that an index entry is relevant for
    # more pages than the one it is located on. Multiple index entries can be
    # present in one annotation, separated by a carriage return character (\r).
    # This function splits annotations up in index entries, formats and sorts
    # them.
    processed = []
    for annot in annotations:
        # grab the important parts from the raw annotation data
        content = annot[0]['content']
        # split annotations into index entries by carriage return characters
        for c in content.split('\r'):
            i = c.find('>')
            # compress the index entries into one string to prepare for the
            # sorting process, using '§§§' as a separation character to split
            # them up again later
            if(i != -1):
                tmp = c[:i-1].lstrip()+'§§§'+str(annot[1])+'-'+c[i+2:]
            else:
                tmp = c.lstrip()+'§§§'+str(annot[1])

            processed.append(tmp.replace('\n', ''))

    # sort the annotations alphabetically and split them up into index contents
    # and page number(s) again
    if(sort):
        processed = sorted(processed, key=sorting_key)
    for i in range(len(processed)):
        processed[i] = processed[i].split('§§§')

    # Merge annotations
    ## Turned out to be unnecessary, but I might need it in the future
    #i = 0
    #while(i < len(processed)):
    #    while(processed[i][0] == processed[i-1][0]):
    #        processed[i-1][1] = str(processed[i-1][1]) + ', ' + str(processed[i][1])
    #        processed.pop(i)
    #    i += 1

    return processed

def export_tsv(annotations, output):
    """
    Save index entries into a tsv (tab-separated values) text file that can be
    imported into Cindex and potentially other indexing software.

    :param annotations: annotations data from process_annotations()
    :param output: name/location of output file
    """

    for annot in annotations:
        annot[0] = annot[0].replace(": ", "\t")
        annot[0] = annot[0].replace(":", "\t")
    file = open(output, 'w', encoding="utf-8")
    for annot in annotations:
        file.write(str(annot[0])+'\t'+str(annot[1])+'\n')
    file.close()
