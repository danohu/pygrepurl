// Build with
// go build -buildmode=c-shared -o trigrams.so trigrams.go

package main

import (
	"C"
	"encoding/json"
	syntax "regexp/syntax"

	index "github.com/google/codesearch/index"
)

//export Trigrams
func Trigrams(str *C.char) *C.char {
	inp := C.GoString(str)
	rxp, _ := syntax.Parse(inp, syntax.Perl)
	info := index.RegexpQuery(rxp)
	asjson, _ := json.Marshal(info)
	return C.CString(string(asjson[:]))
}

func main() {}
