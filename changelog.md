# Changelog

## v0.3.1
    • Fixed the FOR logic in object logic
    • Edited output

## v0.3.0
    • Added
        • Using '<<' at the beginning enables string builder
            • Use '&' to split values and combine variables
            • You can have a look at 'data/card_designs/yu-gi-oh_tct.json' for an example
        • Added the 'logic' key to objects
            • Can be used for 'FOR' or 'IF' statements
            • untested and not guarenteed to function correctly

    • Changed
        • Formulas are now defined by '>>' at the beginning

## v0.2.1-alpha
    • Added
        • Advanced Formulas
            • use any kind of formulas: (! / % / int / float)
                • requires '&' at the beginning of the string
            • old and simpler variant still supported

## v0.2.0-alpha
    • Added
        • Objects:
            • Text
                • Custom Font
                • Custom Fontsize
                • Automatic or Manual linebreak
                ! Only supports Latin characters

            • Images
                • Custom image paths
                • Custom pixel placing and width
                • Align
                    • center
                    • left
                    • right
                • Anchor Calculation:
                    • lt = Left Top
                    • mm = Middle Middle
                    • rb = Right Bottom
                    • rt = Right Top
            
        • Formulas
            + "!50" = 100% width - 50 pixel

    • Quality of life features
        • You can now dynamically set data paths in the "folders" dictionary
        • Using true file path
            • Enables support for linux and Mac OS

## v0.1.1-alpha
    + Card Creation
    • Objects:
        + Rectangle
