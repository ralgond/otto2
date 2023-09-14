package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"

	"github.com/ralgond/topk"
)

func add_one(nested_map map[int]map[int]int, i int, j int) {
	_, ok := nested_map[i]
	if ok == false {
		nested_map[i] = make(map[int]int)
	}
	map_i, ok := nested_map[i]
	cnt_j, ok := map_i[j]
	if ok == false {
		map_i[j] = 1
	} else {
		map_i[j] = cnt_j + 1
	}
}

func from_freq_2_topk(nested map[int]map[int]int, topN int, at_least_covisit int, file *os.File) {
	writer := bufio.NewWriter(file)
	for item_id, item_map := range nested {
		_topk := topk.NewTOPK(topN)
		for item_id2, cnt := range item_map {
			if cnt < at_least_covisit {
				continue
			}
			_topk.Add2(item_id2, cnt)
		}
		s := fmt.Sprintf("%d\t%s\n", item_id, _topk.Dumps())
		writer.WriteString(s)
		writer.Flush()
	}
}

func main() {
	nested := make(map[int]map[int]int)

	// open the file
	file, err := os.Open(os.Args[1])

	//handle errors while opening
	if err != nil {
		log.Fatalf("Error when opening file: %s", err)
	}

	scanner := bufio.NewScanner(file)

	// read line by line
	for scanner.Scan() {
		var line = scanner.Text()
		var ss = strings.Split(line, ",")
		for i := 0; i < len(ss); i++ {
			vi, _ := strconv.Atoi(ss[i])
			for j := i + 1; j < len(ss); j++ {
				vj, _ := strconv.Atoi(ss[j])

				add_one(nested, vi, vj)
				add_one(nested, vj, vi)
			}
		}
	}

	// handle first encountered error while reading
	if err := scanner.Err(); err != nil {
		log.Fatalf("Error while reading file: %s", err)
	}
	file.Close()

	file, err = os.OpenFile("./data/step_2_result.txt", os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0666)

	from_freq_2_topk(nested, 100, 5, file)

	defer file.Close()

	// for k, v := range nested {
	// 	fmt.Println(k, v)
	// }
}
