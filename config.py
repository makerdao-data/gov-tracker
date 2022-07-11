#  Copyright 2021 DAI Foundation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import os
from dotenv import load_dotenv
import sqlalchemy

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

# load secrets from the local .env file
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Snowflake connection
SNOWFLAKE_CONNECTION = dict(
    account=os.environ.get("SNOWFLAKE_ACCOUNT"),
    user=os.environ.get("SNOWFLAKE_USER"),
    password=os.environ.get("SNOWFLAKE_PASS"),
    role=os.environ.get("SNOWFLAKE_ROLE"),
    warehouse=os.environ.get("SNOWFLAKE_WAREHOUSE"),
)


connect_url = sqlalchemy.engine.url.URL(
    "snowflake",
    username=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASS"),
    host=os.getenv("SNOWFLAKE_ACCOUNT"),
    query={
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "role": os.getenv("SNOWFLAKE_ROLE"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    },
)


MAP = {
    "DC-IAM": {
        "address": "<a href='https://etherscan.io/address/0xc7bdd1f2b16447dcf3de045c4a039a60ec2f0ba3'>0xc7bdd1f2b16447dcf3de045c4a039a60ec2f0ba3</a>",
        "contract_name": "DssAutoLine",
        "category": "Debt Ceiling Instant Access Module",
        "alias": "DC-IAM",
        "type" : "ilk",
        "info": ""
    },
    "CAT": {
        "address": "<a href='https://etherscan.io/address/0xc7bdd1f2b16447dcf3de045c4a039a60ec2f0ba3'>0xc7bdd1f2b16447dcf3de045c4a039a60ec2f0ba3</a>",
        "contract_name": "Cat",
        "category": "Dai Stablecoin System - Liquidation 1.0 Module",
        "alias": "CAT",
        "type" : "system-wide",
        "info": ""
    },
    "VOW": {
        "address": "<a href='https://etherscan.io/address/0xa950524441892a31ebddf91d3ceefa04bf454466'>0xa950524441892a31ebddf91d3ceefa04bf454466</a>",
        "contract_name": "Vow",
        "category": "Dai Stablecoin System - System Stabilizer Module",
        "alias": "VOW",
        "type" : "system-wide",
        "info": ""
    },
    "D3M": {
        "address": "<a href='https://etherscan.io/address/0xa13c0c8eb109f5a13c6c90fc26afb23beb3fb04a'>0xa13c0c8eb109f5a13c6c90fc26afb23beb3fb04a</a>",
        "contract_name": "DssDirectDepositAaveDai",
        "category": "Direct Deposit Module",
        "alias": "D3M",
        "type" : "ilk",
        "info": ""
    },
    "VAT": {
        "address": "<a href='https://etherscan.io/address/0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b'>0x35d1b3f3d7966a1dfe207aa4514c12a259a0492b</a>",
        "contract_name": "Vat",
        "category": "Dai Stablecoin System - Core System Accounting",
        "alias": "VAT",
        "type" : "ilk",
        "info": ""
    },
    "SPOTTER": {
        "address": "<a href='https://etherscan.io/address/0x65c79fcb50ca1594b025960e539ed7a9a6d434a3'>0x65c79fcb50ca1594b025960e539ed7a9a6d434a3</a>",
        "contract_name": "Spotter",
        "category": "Dai Stablecoin System - Core Module",
        "alias": "SPOTTER",
        "type" : "ilk",
        "info": ""
    },
    "JUG": {
        "address": "<a href='https://etherscan.io/address/0x19c0976f590d67707e62397c87829d896dc0f1f1'>0x19c0976f590d67707e62397c87829d896dc0f1f1</a>",
        "contract_name": "Jug",
        "category": "Dai Stablecoin System - Rates Module",
        "alias": "JUG",
        "type" : "ilk",
        "info": ""
    },
    "GSM": {
        "address": "<a href='https://etherscan.io/address/0xbb856d1742fd182a90239d7ae85706c2fe4e5922'>0xbb856d1742fd182a90239d7ae85706c2fe4e5922</a>",
        "contract_name": "End",
        "category": "Governance Module",
        "alias": "GSM",
        "type" : "system-wide",
        "info": ""
    },
    "ESM": {
        "address": "<a href='https://etherscan.io/address/0x09e05ff6142f2f9de8b6b65855a1d56b6cfe4c58'>0x09e05ff6142f2f9de8b6b65855a1d56b6cfe4c58</a>",
        "contract_name": "Esm",
        "category": "Emergency Shutdown Module",
        "alias": "ESM",
        "type" : "system-wide",
        "info": ""
    },
    "PSM": {
        "address": "<a href='",
        "contract_name": "DssPsm",
        "category": "Peg Stability Module",
        "alias": "PSM",
        "type" : "ilk",
        "info": ""
    },
    "FLOPPER": {
        "address": "<a href='https://etherscan.io/address/0xa41b6ef151e06da0e34b009b86e828308986736d'>0xa41b6ef151e06da0e34b009b86e828308986736d</a>",
        "contract_name": "Flopper",
        "category": "Dai Stablecoin System - System Stabilizer Module",
        "alias": "FLOPPER",
        "type" : "system-wide",
        "info": "Debt Auctons"
    },
    "FLIPPER": {
        "address": "<a href='",
        "contract_name": "Flipper",
        "category": "Dai Stablecoin System - Collateral Auction Module",
        "alias": "FLIPPER",
        "type" : "ilk",
        "info": "Collateral Auctions"
    },
    "FLAPPER": {
        "address": "<a href='https://etherscan.io/address/0xa4f79bc4a5612bdda35904fdf55fc4cb53d1bff6'>0xa4f79bc4a5612bdda35904fdf55fc4cb53d1bff6</a>",
        "contract_name": "Flapper",
        "category": "Dai Stablecoin System - System Stabilizer Module",
        "alias": "FLAPPER",
        "type" : "system-wide",
        "info": "Surplus Auctions"
    },
    "DSPAUSE": {
        "address": "<a href='https://etherscan.io/address/0xbe286431454714f511008713973d3b053a2d38f3'>0xbe286431454714f511008713973d3b053a2d38f3</a>",
        "contract_name": "DssPause",
        "category": "Governance Module",
        "alias": "DSPAUSE",
        "type" : "system-wide",
        "info": "Surplus Auctions"
    },
    "DOG": {
        "address": "<a href='https://etherscan.io/address/0x135954d155898d42c90d2a57824c690e0c7bef1b'>0x135954d155898d42c90d2a57824c690e0c7bef1b</a>",
        "contract_name": "Dog",
        "category": "Dai Stablecoin System - Liquidation 2.0 Module",
        "alias": "DOG",
        "type" : "ilk",
        "info": ""
    },
    "CLIPPER": {
        "address": "",
        "contract_name": "Clip",
        "category": "Dai Stablecoin System - Liquidation 2.0 Module",
        "alias": "CLIPPER",
        "type" : "ilk",
        "info": ""
    }
}