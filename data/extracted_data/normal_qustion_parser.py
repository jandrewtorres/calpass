import argparse
import pathlib
import re
import json

question_answer_pattern = re.compile(r"^[\w\s]*\|\s*([^?|]*)(?:[?\s|.]*)\s*(.*)")
variable_pattern = re.compile(r"\[([^\[\]]*)\]")

day_pattern = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)
time_pattern = re.compile(r'(\d{1,2})(?=pm|am|:)(?::(\d{2}))?(am|pm)?', re.IGNORECASE)
words_pattern = re.compile(r'([^\s\w]|_)+', re.IGNORECASE)

def type_str_from_answer(text, types):
    match = variable_pattern.findall(text)
    try:
        if len(match) > 0:
            found_type = None
            for v in match:
                varn = v.replace('[', '').replace(']', '')
                if varn in types:
                    found_type = types[varn]
                    break
            if found_type is None:
                raise Exception(f'untyped variable{match}')
            return found_type
        else:
            raise Exception('no match')
    except Exception as e:
        print(f'failed to type variable for \'{text}\': {str(e)}')
        return None
    

def parse_example_question_file(file, var_map=None, replace=None, types=None):
    variables = set()
    questions = []
    answers = []
    replace = {} if replace is None else replace
    types = {} if types is None else types

    if file.exists() and file.is_file():
        for line in file.open().readlines():
            line = line.strip()
            # print(line)
            question_answer = question_answer_pattern.match(line)
            if question_answer is not None:
                groups = question_answer.groups()
                question = groups[0]
                answer = groups[1]

                for r,s in replace.items():
                    question = re.sub(r, s, question, flags=re.IGNORECASE)
                    answer = re.sub(r, s, answer, flags=re.IGNORECASE)

                question = re.sub(r"\s+", ' ', question)
                answer = re.sub(r"\s+", ' ', answer)

                # help out questions with specific data points in them
                question = day_pattern.sub('[day]', question)
                answer = day_pattern.sub('[day]', answer)
                # TODO more to check for courses/numbers/times

                # variable replacement
                def var_replacer(string):
                    for v in variable_pattern.findall(string):
                        mqvar = var_map.get(v.lower()) if var_map else None
                        if mqvar:
                            string = re.sub(f'\[{v}\]', mqvar, string, flags=re.IGNORECASE)
                        else:
                            string = re.sub(f'\[{v}\]', f'[{v.lower()}]', string, flags=re.IGNORECASE)
                    va = variable_pattern.findall(string)
                    return string, va
                question, var_q = var_replacer(question)
                answer, var_a = var_replacer(answer)
                # print(question)
                # print(f'{groups[0]} -> {question}')
                questions.append(question)
                answers.append((answer, type_str_from_answer(answer, types)))
                for v in [y for x in (var_q, var_a) for y in x]:
                    variables.add(v.lower())
            else:
                if len(line) > 0:
                    print(f'non conforming line: {line}')
                    
    else:
        raise Exception(f"no file {file.absolute()}")

    return variables, questions, answers


def main():
    parser = argparse.ArgumentParser(description='question parser')
    parser.add_argument(dest='infile', metavar='I', type=str, help='input file')

    parser.add_argument('--dump-vars', dest='vars', action='store_true', required=False, help='output set of var strings in file')
    parser.add_argument('--var-file', type=str, required=False, help='file to load or store variable mappings', metavar='V', dest='varfile')
    parser.add_argument('--out', type=str, required=False, help='file to store parsed questions (json)', metavar='o', dest='outfile')

    args = parser.parse_args()
    # for f in pathlib.Path(args.indir).glob('*.txt'):
    #     print(f.name)
    file = pathlib.Path(args.infile)
    if not file.exists():
        print(f'no file {file.absolute()}')
        exit(-1)

    var_map = None

    if args.varfile:
        varfile = pathlib.Path(args.varfile)
        if varfile.exists():
            try:
                var_map = json.load(varfile.open('r'))
                print(f'loaded var_map file {varfile.absolute()}')
                assert(isinstance(var_map, dict))
            except json.JSONDecodeError as e:
                print(f'invalid var_map file {e}')


    var, questions, answers = parse_example_question_file(file, var_map["map"], var_map["replace"], var_map['types'])

    if args.varfile:
        if var_map is None:
            var_map = {}
            var_map['map'] = {}
            var_map['replace'] = {}
            var_map['types'] = {}
        for v in var:
            if v not in var_map['map']:
                var_map['map'].update({v : None})
            if var_map['map'][v] is None:
                if v not in var_map['types']:
                    var_map['types'].update({v : None})
        if not varfile.exists():
            varfile.touch(mode=0o755)
        with varfile.open(mode='w') as wo:
            wo.write(json.dumps(var_map, indent=4))

    if args.vars:
        print(list(var))

    if args.outfile is None:
        for q in questions:
            print(q)
    else:
        outfile = pathlib.Path(args.outfile)
        outfile.touch(mode=0o755)
        if outfile.exists() and outfile.is_file():
            with outfile.open(mode='w') as wo:
                wo.write(json.dumps(list(zip(questions, answers)), indent=4))
        else:
            print(f'{outfile.absolute()} is not a valid destination')
            exit(-1)

    


if __name__ == "__main__":
    main()