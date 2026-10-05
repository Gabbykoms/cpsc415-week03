"""Run the same five cases against CHAT_MODEL; no retries or output repairs."""
import json
from pathlib import Path
import sys
from classifier import CATEGORIES, URGENCIES, ClassificationError, classify, configuration


def load_cases():
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    if not isinstance(cases, list) or len(cases) != 5:
        raise ValueError('cases.json must contain exactly five cases')
    ids = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValueError('Every case must be an object')
        for field in ('id', 'message', 'purpose'):
            if not isinstance(case.get(field), str) or not case[field].strip():
                raise ValueError(f'Each case needs a nonempty {field}')
        if case['id'] in ids:
            raise ValueError('Case IDs must be unique')
        ids.add(case['id'])
        for field, allowed in (('categories', CATEGORIES), ('urgencies', URGENCIES)):
            values = case.get(field)
            if not isinstance(values, list) or not values or any(
                    not isinstance(value, str) or value not in allowed for value in values):
                raise ValueError(f'Invalid case {field}')
    return cases


def main():
    try:
        config, cases = configuration(), load_cases()
    except (ValueError, OSError) as error:
        print(f'Setup error: {error}', file=sys.stderr)
        return 2
    totals = {'prompt_tokens': 0, 'completion_tokens': 0}
    missing = dict.fromkeys(totals, 0)
    passed = 0
    print(f'Model: {config[2]}', flush=True)
    for case in cases:
        try:
            result, usage = classify(case['message'], config)
            ok = result['category'] in case['categories'] and result['urgency'] in case['urgencies']
            detail = json.dumps(result)
            if not ok:
                detail += f"; expected categories={case['categories']}, urgencies={case['urgencies']}"
        except ClassificationError as error:
            ok, detail, usage = False, str(error), error.usage
        passed += int(ok)
        print(f"{'PASS' if ok else 'FAIL'} {case['id']}: {detail}", flush=True)
        for field in totals:
            value = usage.get(field)
            if type(value) is int and value >= 0:
                totals[field] += value
            else:
                missing[field] += 1
    print(f'Summary: model={config[2]} passed={passed}/{len(cases)}')
    for field, total in totals.items():
        suffix = f" (partial; unavailable for {missing[field]} cases)" if missing[field] else ''
        print(f'{field}: {total}{suffix}')
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    sys.exit(main())
