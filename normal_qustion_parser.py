import argparse
import pathlib
import re
import json

def parse_file(file, var_map=None):
    question_answer_pattern = re.compile(r"^[\w\s]*\|\s*([^?|.]*)(?:[?\s|.]*)\s*(.*)")
    variable_pattern = re.compile(r"\[([^\[\]]*)\]")

    day_pattern = re.compile(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", re.IGNORECASE)

    variables = set()
    questions = []

    if file.exists() and file.is_file():
        for line in file.open().readlines():
            line = line.strip()
            # print(line)
            question_answer = question_answer_pattern.match(line)
            if question_answer is not None:
                groups = question_answer.groups()
                question = groups[0]
                answer = groups[1]
                question = re.sub(r"\s+", ' ', question)

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
                question, var = var_replacer(question)
                # answer = var_replacer(answer)
                print(question)
                # print(f'{groups[0]} -> {question}')
                questions.append(question)
                for v in var:
                    variables.add(v.lower())
            else:
                if len(line) > 0:
                    print(f'non conforming line: {line}')
                    
    else:
        raise Exception(f"no file {file.absolute()}")

    return variables, questions


def main():
    parser = argparse.ArgumentParser(description='question parser')
    parser.add_argument(dest='infile', metavar='I', type=str, help='input file')

    parser.add_argument('--dump-vars', dest='vars', action='store_true', required=False, help='output set of var strings in file')
    parser.add_argument('--var-file', type=str, required=False, help='file to load or store variable mappings', metavar='V', dest='varfile')

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


    var, questions = parse_file(file, var_map)

    if args.varfile and not varfile.exists():
        if var_map is None:
            var_map = {}
            for v in var:
                var_map.update({v : None})
        varfile.touch(mode=0o755)
        with varfile.open(mode='w') as wo:
            wo.write(json.dumps(var_map))

    if args.vars:
        print(list(var))

    


if __name__ == "__main__":
    main()