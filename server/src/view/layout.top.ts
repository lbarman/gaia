
/* tslint:disable */
// This file was generated from a topside template.
// Do not edit this file, edit the original template instead.

import * as __escape from 'escape-html';
__escape;


export interface __Section {
    (parent: () => string): () => string;
}
export type __Params = {

} 

function __identity<T>(t: T): T {
    return t;
}
__identity;

function __safeSection(section?: __Section): __Section {
        return section ? section : __identity;
}
__safeSection;

export default function(__params?: __Params, __childSections?: {
            'styles'?: __Section;
            'content'?: __Section;
        }): string {


    let __safeChildSections: {
            'styles'?: __Section;
            'content'?: __Section;
        } = __childSections || {};
    __safeChildSections;
    const __sections: {
            'styles': __Section;
            'content': __Section;
        } = {
        "styles": __safeSection(__safeChildSections["styles"]),
        "content": __safeSection(__safeChildSections["content"])
    };
    __sections;
    const __text = "<!DOCTYPE html>\n<html lang=\"en\">\n    <head>\n        <meta charset=\"UTF-8\">\n        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n        <meta http-equiv=\"X-UA-Compatible\" content=\"ie=edge\">\n        <meta http-equiv=\"Pragma\" content=\"no-cache\">\n\n        <title>Bonevouetta HotSprings</title>\n\n        <link rel=\"stylesheet\" href=\"/css/normalize.css\">\n        <link rel=\"stylesheet\" href=\"/css/sakura.css\">\n        <link rel=\"stylesheet\" href=\"/css/index.css\">\n\n        " + __sections["styles"](() => "")() + "\n    </head>\n    <body>\n        <script src=\"/js/breadcrumbs.js\"></script>\n\n        <div id=\"subbody\">\n            <div id=\"header\">\n                <h1>Bonnevouetta HotSprings</h1>\n            </div>\n            \n            <div id=\"content\">\n            <!-- START TEMPLATE CONTENT -->\n            " + __sections["content"](() => "")() + "\n            <!-- END TEMPLATE CONTENT -->\n            </div>\n        </div>\n        <svg>\n            <defs>\n                <symbol id=\"icon-checkmark-outline\" viewBox=\"0 0 20 20\">\n                <title>checkmark-outline</title>\n                <path d=\"M2.93 17.070c-1.884-1.821-3.053-4.37-3.053-7.193 0-5.523 4.477-10 10-10 2.823 0 5.372 1.169 7.19 3.050l0.003 0.003c1.737 1.796 2.807 4.247 2.807 6.947 0 5.523-4.477 10-10 10-2.7 0-5.151-1.070-6.95-2.81l0.003 0.003zM15.66 15.66c1.449-1.449 2.344-3.45 2.344-5.66 0-4.421-3.584-8.004-8.004-8.004-2.21 0-4.211 0.896-5.66 2.344v0c-1.449 1.449-2.344 3.45-2.344 5.66 0 4.421 3.584 8.004 8.004 8.004 2.21 0 4.211-0.896 5.66-2.344v0zM6.7 9.29l2.3 2.31 4.3-4.3 1.4 1.42-5.7 5.68-3.7-3.7 1.4-1.42z\"></path>\n                </symbol>\n            </defs>\n        </svg>\n    </body>\n</html>";
    __text;
    return __text;
};
//# sourceMappingURL=layout.top.ts.map