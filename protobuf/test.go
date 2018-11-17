package main

import (
	"log"
	"io/ioutil"
	"fmt"

	"github.com/golang/protobuf/proto"
	"github.com/lbarman/config"
)

func main() {
	data, err := ioutil.ReadFile("test/out_python") // b has type []byte
	if err != nil {
		log.Fatal(err)
	}

	config := &gaia.Config{}
	err = proto.Unmarshal(data, config)
	if err != nil {
		log.Fatal("unmarshaling error: ", err)
	}
	fmt.Printf("%+v\n", config)	
}