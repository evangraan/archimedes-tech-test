# Archimedes tech test

## Instructions

We know that you're busy and we wanted to give you the chance to show us what you can do, so we designed this task to take no longer than 2 hours of your time.

You are free to use any language/framework you are comfortable with.

Please feel free to reach us out if you have any questions/doubts.

To send us your solution you can do any of the following:
- send us the link of your git repo (if it's a private repo, please give us access)
- send us a zip git repo
- fork this repo as a private fork and give us the access

## Context

In the Archimedes team, one of our typical activities might look like the following:
- ingest input data
- enrich with various external/internal information
- present the transformed data

This tech test is a simplified sample from one of our real systems.

## Task

Build a program which from two sources of data (calls and network operators) generates a CSV report.

### Input: calls

The first source is a JSON document containing phone calls:

```json
{
  "data": [
    {
      "type": "call",
      "id": "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b",
      "attributes": {
        "date": "2020-10-12T07:20:50.52Z",
        "riskScore": 0.431513435443,
        "number": "+44123456789",
        "greenList": true,
        "redList": false
      }
    },
    {
      "type": "call",
      "id": "8f1b1354-26d2-4e16-9582-9156a0d9a5de",
      "attributes": {
        "date": "2019-10-12T07:20:50.52Z",
        "riskScore": 0.123444,
        "number": "+44123456789",
        "greenList": false,
        "redList": true
      }
    }
  ]
}
```

Where:
| field                | type   | description                                                    | example                                |
|----------------------|--------|----------------------------------------------------------------|----------------------------------------|
| type                 | string | always "call"                                                  | "call"                                 |
| id                   | string | UUID                                                           | "8f1b1354-26d2-4e16-9582-9156a0d9a5de" |
| attributes.date      | string | UTC date in RFC 3339 format                                    | "2019-10-12T07:20:50.52Z"              |
| attributes.riskScore | float  | number between 0.0 (not risky)  and 1.0 (potential fraud call) | 0.1231351351435                        |
| attributes.number    | string | phone number in E164 format                                    | +4467464311354153                      |
| attributes.greenList | bool   | the call is not risky regardless of the risk score             | true                                   |
| attributes.redList   | bool   | the call is fraud regardless of the risk score                 | false                                  |

### Input: operators

The second source is a JSON document containing phone operators:

```json
{
  "data": [
    {
      "type": "operator",
      "id": "2c4fae60-cf43-4f27-869e-a9ed8b0ca25b",
      "attributes": {
        "prefix": "1000",
        "operator": "Vodafone"
      }
    },
    {
      "type": "call",
      "id": "8f1b1354-26d2-4e16-9582-9156a0d9a5de",
      "attributes": {
        "prefix": "2000",
        "operator": "EE"
      }
    }
  ]
}
```

Where:
| field               | type   | description                    | example                                |
|---------------------|--------|--------------------------------|----------------------------------------|
| type                | string | always "operator"              | "operator"                             |
| id                  | string | UUID                           | "8f1b1354-26d2-4e16-9582-9156a0d9a5de" |
| attributes.prefix   | string | prefix range - see below       | "2000"                                 |
| attributes.operator | string | the name of the phone operator | "Vodafone"                             |

If the prefix range is "2000", it means that a national number starting with that prefix belongs to that phone operator:
- `+442143999888`: belongs to the operator, it can be broken down as `+44-2143-999888` and `2143` is in the range 2000-2999
- `+448423666777`: does not belong to the operator, it can be broken down as `+44-8423-666777` and `8423` is not in the range 2000-2999

### Output

The program generates the following CSV from the 2 sources of data:
```csv
id,date,number,operator,riskScore
2c4fae60-cf43-4f27-869e-a9ed8b0ca25b,2020-10-12,+44123,Vodafone,0.0
8f1b1354-26d2-4e16-9582-9156a0d9a5de,2019-10-13,+44654,Unknown,1.0
db48da6c-6cb8-43d5-9637-5906b295fd20,2019-11-12,+99132,EE,0.3
911ea345-c58c-4688-bd9a-725263a1540b,2020-11-12,Withheld,Unknown,0.9
```

The operator field is obtained by a lookup in the operators JSON based on the number phone.

The rules for the risk score calculation are:
- round up to 1 DP
- if on the green list, the value is 0.0
- if on the red list, the value is 1.0
- being on the green list has precedence on the red list

Misc rules:
- the target date format for the CSV is: `YYYY-MM-DD`
- if the operator cannot be found, "Unknown" should be displayed as the operator field
- if the number is absent, "Withheld" should be displayed as the number field
- the calls are ordered by ascending date

## What we expect

- clean code practices
- relevant usage of software design patterns
- relevant test coverage
- simple README to explain how to run your program
- regular committing to see your thoughts process

## Input data

- the calls JSON data file: `data/calls.json`
- the operators JSON data file: `data/operators.json`

