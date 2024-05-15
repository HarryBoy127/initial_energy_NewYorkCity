{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import re\n",
    "from autocorrect import Speller\n",
    "import pandas as pd\n",
    "import psycopg2\n",
    "import datetime as dt\n",
    "import numpy as np\n",
    "import seaborn as sns\n",
    " \n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "import warnings\n",
    "warnings.filterwarnings(\"ignore\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Development Name</th>\n",
       "      <th>Borough</th>\n",
       "      <th>Account Name</th>\n",
       "      <th>Location</th>\n",
       "      <th>Meter AMR</th>\n",
       "      <th>Meter Scope</th>\n",
       "      <th>TDS #</th>\n",
       "      <th>EDP</th>\n",
       "      <th>RC Code</th>\n",
       "      <th>Funding Source</th>\n",
       "      <th>...</th>\n",
       "      <th>Meter Number</th>\n",
       "      <th>Estimated</th>\n",
       "      <th>Current Charges</th>\n",
       "      <th>Rate Class</th>\n",
       "      <th>Bill Analyzed</th>\n",
       "      <th>Consumption (KWH)</th>\n",
       "      <th>KWH Charges</th>\n",
       "      <th>Consumption (KW)</th>\n",
       "      <th>KW Charges</th>\n",
       "      <th>Other charges</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BLD 05</td>\n",
       "      <td>NONE</td>\n",
       "      <td>BLD 01 to 07</td>\n",
       "      <td>118.0</td>\n",
       "      <td>248</td>\n",
       "      <td>B011800</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>...</td>\n",
       "      <td>7223256</td>\n",
       "      <td>N</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>GOV/NYC/068</td>\n",
       "      <td>Yes</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>7387.97</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>5200.85</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BLD 05</td>\n",
       "      <td>NONE</td>\n",
       "      <td>BLD 01 to 07</td>\n",
       "      <td>118.0</td>\n",
       "      <td>248</td>\n",
       "      <td>B011800</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>...</td>\n",
       "      <td>7223256</td>\n",
       "      <td>N</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>GOV/NYC/068</td>\n",
       "      <td>Yes</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>6607.87</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>5036.47</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>BLD 05</td>\n",
       "      <td>NONE</td>\n",
       "      <td>BLD 01 to 07</td>\n",
       "      <td>118.0</td>\n",
       "      <td>248</td>\n",
       "      <td>B011800</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>...</td>\n",
       "      <td>7223256</td>\n",
       "      <td>N</td>\n",
       "      <td>13904.98</td>\n",
       "      <td>GOV/NYC/068</td>\n",
       "      <td>Yes</td>\n",
       "      <td>103200.0</td>\n",
       "      <td>5919.55</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>5177.43</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>3 rows × 27 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "  Development Name Borough Account Name Location Meter AMR   Meter Scope  \\\n",
       "0            ADAMS   BRONX        ADAMS   BLD 05      NONE  BLD 01 to 07   \n",
       "1            ADAMS   BRONX        ADAMS   BLD 05      NONE  BLD 01 to 07   \n",
       "2            ADAMS   BRONX        ADAMS   BLD 05      NONE  BLD 01 to 07   \n",
       "\n",
       "   TDS #  EDP  RC Code Funding Source  ... Meter Number Estimated  \\\n",
       "0  118.0  248  B011800        FEDERAL  ...      7223256         N   \n",
       "1  118.0  248  B011800        FEDERAL  ...      7223256         N   \n",
       "2  118.0  248  B011800        FEDERAL  ...      7223256         N   \n",
       "\n",
       "   Current Charges   Rate Class Bill Analyzed Consumption (KWH)  KWH Charges  \\\n",
       "0         15396.82  GOV/NYC/068           Yes          128800.0      7387.97   \n",
       "1         14556.34  GOV/NYC/068           Yes          115200.0      6607.87   \n",
       "2         13904.98  GOV/NYC/068           Yes          103200.0      5919.55   \n",
       "\n",
       "  Consumption (KW) KW Charges  Other charges  \n",
       "0            216.0     2808.0        5200.85  \n",
       "1            224.0     2912.0        5036.47  \n",
       "2            216.0     2808.0        5177.43  \n",
       "\n",
       "[3 rows x 27 columns]"
      ]
     },
     "execution_count": 41,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_raw = pd.read_csv(\"./data/raw/Electric_Consumption_And_Cost__2010_-_Feb_2023__20240417.csv\")\n",
    "energy_raw.head(3)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['Development Name', 'Borough', 'Account Name', 'Location', 'Meter AMR',\n",
       "       'Meter Scope', 'TDS #', 'EDP', 'RC Code', 'Funding Source', 'AMP #',\n",
       "       'Vendor Name', 'UMIS BILL ID', 'Revenue Month', 'Service Start Date',\n",
       "       'Service End Date', '# days', 'Meter Number', 'Estimated',\n",
       "       'Current Charges', 'Rate Class', 'Bill Analyzed', 'Consumption (KWH)',\n",
       "       'KWH Charges', 'Consumption (KW)', 'KW Charges', 'Other charges'],\n",
       "      dtype='object')"
      ]
     },
     "execution_count": 42,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_raw.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(447849, 27)"
      ]
     },
     "execution_count": 43,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_raw.shape"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Data Cleaning Tasks \n",
    "\n",
    "#### Task 1: Identify and Remove Irrelevant Features"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Borough</th>\n",
       "      <th>Account Name</th>\n",
       "      <th>Meter Number</th>\n",
       "      <th>Funding Source</th>\n",
       "      <th>Current Charges</th>\n",
       "      <th>Consumption (KWH)</th>\n",
       "      <th>KWH Charges</th>\n",
       "      <th>Consumption (KW)</th>\n",
       "      <th>KW Charges</th>\n",
       "      <th>Revenue Month</th>\n",
       "      <th>Service Start Date</th>\n",
       "      <th>Service End Date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>7387.97</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01</td>\n",
       "      <td>12/24/09</td>\n",
       "      <td>1/26/10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>6607.87</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02</td>\n",
       "      <td>1/26/10</td>\n",
       "      <td>2/25/10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>13904.98</td>\n",
       "      <td>103200.0</td>\n",
       "      <td>5919.55</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-03</td>\n",
       "      <td>2/25/10</td>\n",
       "      <td>3/26/10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14764.04</td>\n",
       "      <td>105600.0</td>\n",
       "      <td>6057.22</td>\n",
       "      <td>208.0</td>\n",
       "      <td>2704.0</td>\n",
       "      <td>2010-04</td>\n",
       "      <td>3/26/10</td>\n",
       "      <td>4/26/10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>13729.54</td>\n",
       "      <td>97600.0</td>\n",
       "      <td>5598.34</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-05</td>\n",
       "      <td>4/26/10</td>\n",
       "      <td>5/24/10</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  Borough Account Name Meter Number Funding Source  Current Charges  \\\n",
       "0   BRONX        ADAMS      7223256        FEDERAL         15396.82   \n",
       "1   BRONX        ADAMS      7223256        FEDERAL         14556.34   \n",
       "2   BRONX        ADAMS      7223256        FEDERAL         13904.98   \n",
       "3   BRONX        ADAMS      7223256        FEDERAL         14764.04   \n",
       "4   BRONX        ADAMS      7223256        FEDERAL         13729.54   \n",
       "\n",
       "   Consumption (KWH)  KWH Charges  Consumption (KW)  KW Charges Revenue Month  \\\n",
       "0           128800.0      7387.97             216.0      2808.0       2010-01   \n",
       "1           115200.0      6607.87             224.0      2912.0       2010-02   \n",
       "2           103200.0      5919.55             216.0      2808.0       2010-03   \n",
       "3           105600.0      6057.22             208.0      2704.0       2010-04   \n",
       "4            97600.0      5598.34             216.0      2808.0       2010-05   \n",
       "\n",
       "  Service Start Date Service End Date  \n",
       "0           12/24/09          1/26/10  \n",
       "1            1/26/10          2/25/10  \n",
       "2            2/25/10          3/26/10  \n",
       "3            3/26/10          4/26/10  \n",
       "4            4/26/10          5/24/10  "
      ]
     },
     "execution_count": 44,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_selected_column =energy_raw[[\"Borough\", \"Account Name\",\"Meter Number\",\"Funding Source\",\"Current Charges\",\\\n",
    "                                     'Consumption (KWH)','KWH Charges', 'Consumption (KW)', 'KW Charges',\\\n",
    "                                     \"Revenue Month\",\"Service Start Date\", \"Service End Date\"]]\n",
    "energy_selected_column.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 1: Remove columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>7387.97</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01</td>\n",
       "      <td>12/24/09</td>\n",
       "      <td>1/26/10</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>6607.87</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02</td>\n",
       "      <td>1/26/10</td>\n",
       "      <td>2/25/10</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  borough account_name serial_number funding_origin  total_bill  \\\n",
       "0   BRONX        ADAMS       7223256        FEDERAL    15396.82   \n",
       "1   BRONX        ADAMS       7223256        FEDERAL    14556.34   \n",
       "\n",
       "   kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month start_date  \\\n",
       "0         128800.0   7387.97           216.0   2808.0    2010-01   12/24/09   \n",
       "1         115200.0   6607.87           224.0   2912.0    2010-02    1/26/10   \n",
       "\n",
       "  end_date  \n",
       "0  1/26/10  \n",
       "1  2/25/10  "
      ]
     },
     "execution_count": 45,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_selected_column.rename(columns= \n",
    "                                {\"Borough\":\"borough\", \n",
    "                                \"Account Name\" :\"account_name\",\n",
    "                                \"Meter Number\":\"serial_number\",\n",
    "                                \"Funding Source\":\"funding_origin\",\n",
    "                                \"Current Charges\":\"total_bill\",\n",
    "                                \"Revenue Month\":\"year_month\",\n",
    "                                \"Consumption (KWH)\": \"kwh_consumption\", # kwh_usage\n",
    "                                \"KWH Charges\": \"kwh_bill\",\n",
    "                                \"Consumption (KW)\":\"kw_consumption\",\n",
    "                                \"KW Charges\": \"kw_bill\",\n",
    "                                \"Service Start Date\":\"start_date\",\n",
    "                                \"Service End Date\":\"end_date\"},inplace = True)\n",
    "\n",
    "energy_selected_column.head(2)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 2: Handle Missing Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "16"
      ]
     },
     "execution_count": 46,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_handle_missing_data = energy_selected_column.copy()\n",
    "energy_handle_missing_data.isnull().sum().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "borough            0\n",
       "account_name       0\n",
       "serial_number      0\n",
       "funding_origin     0\n",
       "total_bill         0\n",
       "kwh_consumption    0\n",
       "kwh_bill           0\n",
       "kw_consumption     0\n",
       "kw_bill            0\n",
       "year_month         0\n",
       "start_date         8\n",
       "end_date           8\n",
       "dtype: int64"
      ]
     },
     "execution_count": 47,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_handle_missing_data.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 48,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>294254</th>\n",
       "      <td>MANHATTAN</td>\n",
       "      <td>LOWER EAST SIDE II</td>\n",
       "      <td>5503302</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-04</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>297117</th>\n",
       "      <td>BROOKLYN</td>\n",
       "      <td>RED HOOK EAST</td>\n",
       "      <td>9956008</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15.96</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-02</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>297120</th>\n",
       "      <td>BROOKLYN</td>\n",
       "      <td>RED HOOK EAST</td>\n",
       "      <td>9956007</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>20.22</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-02</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>337554</th>\n",
       "      <td>MANHATTAN</td>\n",
       "      <td>LOWER EAST SIDE II</td>\n",
       "      <td>5503302</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-04</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>337555</th>\n",
       "      <td>MANHATTAN</td>\n",
       "      <td>LOWER EAST SIDE II</td>\n",
       "      <td>5503302</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>0.04</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-06</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>337556</th>\n",
       "      <td>MANHATTAN</td>\n",
       "      <td>LOWER EAST SIDE II</td>\n",
       "      <td>5503302</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>0.00</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-05</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>347588</th>\n",
       "      <td>BROOKLYN</td>\n",
       "      <td>RED HOOK EAST</td>\n",
       "      <td>9956008</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15.96</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-02</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>347592</th>\n",
       "      <td>BROOKLYN</td>\n",
       "      <td>RED HOOK EAST</td>\n",
       "      <td>9956007</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>20.22</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>2020-02</td>\n",
       "      <td>NaN</td>\n",
       "      <td>NaN</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "          borough        account_name serial_number funding_origin  \\\n",
       "294254  MANHATTAN  LOWER EAST SIDE II       5503302        FEDERAL   \n",
       "297117   BROOKLYN       RED HOOK EAST       9956008        FEDERAL   \n",
       "297120   BROOKLYN       RED HOOK EAST       9956007        FEDERAL   \n",
       "337554  MANHATTAN  LOWER EAST SIDE II       5503302        FEDERAL   \n",
       "337555  MANHATTAN  LOWER EAST SIDE II       5503302        FEDERAL   \n",
       "337556  MANHATTAN  LOWER EAST SIDE II       5503302        FEDERAL   \n",
       "347588   BROOKLYN       RED HOOK EAST       9956008        FEDERAL   \n",
       "347592   BROOKLYN       RED HOOK EAST       9956007        FEDERAL   \n",
       "\n",
       "        total_bill  kwh_consumption  kwh_bill  kw_consumption  kw_bill  \\\n",
       "294254        0.00              0.0       0.0             0.0      0.0   \n",
       "297117       15.96              0.0       0.0             0.0      0.0   \n",
       "297120       20.22              0.0       0.0             0.0      0.0   \n",
       "337554        0.00              0.0       0.0             0.0      0.0   \n",
       "337555        0.04              0.0       0.0             0.0      0.0   \n",
       "337556        0.00              0.0       0.0             0.0      0.0   \n",
       "347588       15.96              0.0       0.0             0.0      0.0   \n",
       "347592       20.22              0.0       0.0             0.0      0.0   \n",
       "\n",
       "       year_month start_date end_date  \n",
       "294254    2020-04        NaN      NaN  \n",
       "297117    2020-02        NaN      NaN  \n",
       "297120    2020-02        NaN      NaN  \n",
       "337554    2020-04        NaN      NaN  \n",
       "337555    2020-06        NaN      NaN  \n",
       "337556    2020-05        NaN      NaN  \n",
       "347588    2020-02        NaN      NaN  \n",
       "347592    2020-02        NaN      NaN  "
      ]
     },
     "execution_count": 48,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_handle_missing_data[energy_handle_missing_data.start_date.isnull()]"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 2: Handle Missing Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 49,
   "metadata": {},
   "outputs": [],
   "source": [
    "columns_to_check= [\"start_date\",\"end_date\"]\n",
    "energy_dropna_columns = energy_handle_missing_data.dropna(subset= columns_to_check)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 50,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "Index: 447841 entries, 0 to 447848\n",
      "Data columns (total 12 columns):\n",
      " #   Column           Non-Null Count   Dtype  \n",
      "---  ------           --------------   -----  \n",
      " 0   borough          447841 non-null  object \n",
      " 1   account_name     447841 non-null  object \n",
      " 2   serial_number    447841 non-null  object \n",
      " 3   funding_origin   447841 non-null  object \n",
      " 4   total_bill       447841 non-null  float64\n",
      " 5   kwh_consumption  447841 non-null  float64\n",
      " 6   kwh_bill         447841 non-null  float64\n",
      " 7   kw_consumption   447841 non-null  float64\n",
      " 8   kw_bill          447841 non-null  float64\n",
      " 9   year_month       447841 non-null  object \n",
      " 10  start_date       447841 non-null  object \n",
      " 11  end_date         447841 non-null  object \n",
      "dtypes: float64(5), object(7)\n",
      "memory usage: 44.4+ MB\n"
     ]
    }
   ],
   "source": [
    "energy_dropna_columns.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 3: fix the data type"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 51,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "borough                    object\n",
       "account_name               object\n",
       "serial_number              object\n",
       "funding_origin             object\n",
       "total_bill                float64\n",
       "kwh_consumption           float64\n",
       "kwh_bill                  float64\n",
       "kw_consumption            float64\n",
       "kw_bill                   float64\n",
       "year_month         datetime64[ns]\n",
       "start_date         datetime64[ns]\n",
       "end_date           datetime64[ns]\n",
       "dtype: object"
      ]
     },
     "execution_count": 51,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_dropna_columns['start_date'] = pd.to_datetime(energy_dropna_columns['start_date'])\n",
    "energy_dropna_columns['end_date'] = pd.to_datetime(energy_dropna_columns['end_date'])\n",
    "\n",
    "\n",
    "energy_dropna_columns['year_month'] = energy_dropna_columns['year_month'].astype(str) + '-01'\n",
    "energy_dropna_columns['year_month'] = pd.to_datetime(energy_dropna_columns['year_month'])\n",
    "#energy_selected_column['revenue_month']  = energy_selected_column['revenue_month'].dt.strftime('%Y-%m-%d')\n",
    "\n",
    "\n",
    "energy_dropna_columns['total_bill'] = energy_dropna_columns['total_bill'].astype(float)\n",
    "energy_dropna_columns['kwh_consumption'] = energy_dropna_columns ['kwh_consumption'].astype(float)\n",
    "energy_dropna_columns['kw_consumption'] = energy_dropna_columns ['kw_consumption'].astype(float)\n",
    "energy_dropna_columns['kwh_consumption'] = energy_dropna_columns ['kwh_consumption'].astype(float)\n",
    "energy_dropna_columns['kwh_bill'] = energy_dropna_columns ['kw_bill'].astype(float)\n",
    "energy_dropna_columns.dtypes\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 52,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>2009-12-24</td>\n",
       "      <td>2010-01-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>2010-01-26</td>\n",
       "      <td>2010-02-25</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>13904.98</td>\n",
       "      <td>103200.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-03-01</td>\n",
       "      <td>2010-02-25</td>\n",
       "      <td>2010-03-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14764.04</td>\n",
       "      <td>105600.0</td>\n",
       "      <td>2704.0</td>\n",
       "      <td>208.0</td>\n",
       "      <td>2704.0</td>\n",
       "      <td>2010-04-01</td>\n",
       "      <td>2010-03-26</td>\n",
       "      <td>2010-04-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>13729.54</td>\n",
       "      <td>97600.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-05-01</td>\n",
       "      <td>2010-04-26</td>\n",
       "      <td>2010-05-24</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  borough account_name serial_number funding_origin  total_bill  \\\n",
       "0   BRONX        ADAMS       7223256        FEDERAL    15396.82   \n",
       "1   BRONX        ADAMS       7223256        FEDERAL    14556.34   \n",
       "2   BRONX        ADAMS       7223256        FEDERAL    13904.98   \n",
       "3   BRONX        ADAMS       7223256        FEDERAL    14764.04   \n",
       "4   BRONX        ADAMS       7223256        FEDERAL    13729.54   \n",
       "\n",
       "   kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month start_date  \\\n",
       "0         128800.0    2808.0           216.0   2808.0 2010-01-01 2009-12-24   \n",
       "1         115200.0    2912.0           224.0   2912.0 2010-02-01 2010-01-26   \n",
       "2         103200.0    2808.0           216.0   2808.0 2010-03-01 2010-02-25   \n",
       "3         105600.0    2704.0           208.0   2704.0 2010-04-01 2010-03-26   \n",
       "4          97600.0    2808.0           216.0   2808.0 2010-05-01 2010-04-26   \n",
       "\n",
       "    end_date  \n",
       "0 2010-01-26  \n",
       "1 2010-02-25  \n",
       "2 2010-03-26  \n",
       "3 2010-04-26  \n",
       "4 2010-05-24  "
      ]
     },
     "execution_count": 52,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_dropna_columns.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Task 4: Clean Textual Data\n",
    "- If applicable, clean textual data by removing extra spaces, correcting typos\n",
    "- standardizing text (e.g., converting to lowercase)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>2009-12-24</td>\n",
       "      <td>2010-01-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>BRONX</td>\n",
       "      <td>ADAMS</td>\n",
       "      <td>7223256</td>\n",
       "      <td>FEDERAL</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>2010-01-26</td>\n",
       "      <td>2010-02-25</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  borough account_name serial_number funding_origin  total_bill  \\\n",
       "0   BRONX        ADAMS       7223256        FEDERAL    15396.82   \n",
       "1   BRONX        ADAMS       7223256        FEDERAL    14556.34   \n",
       "\n",
       "   kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month start_date  \\\n",
       "0         128800.0    2808.0           216.0   2808.0 2010-01-01 2009-12-24   \n",
       "1         115200.0    2912.0           224.0   2912.0 2010-02-01 2010-01-26   \n",
       "\n",
       "    end_date  \n",
       "0 2010-01-26  \n",
       "1 2010-02-25  "
      ]
     },
     "execution_count": 53,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_clean_textual_data = energy_dropna_columns.copy()\n",
    "energy_clean_textual_data.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert to lowercase\n",
    "energy_clean_textual_data['borough'] = energy_clean_textual_data['borough'].str.lower()\n",
    "energy_clean_textual_data['account_name'] = energy_clean_textual_data['account_name'].str.lower()\n",
    "energy_clean_textual_data['funding_origin'] = energy_clean_textual_data['funding_origin'].str.lower()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Remove extra spaces\n",
    "energy_clean_textual_data['borough'] = energy_clean_textual_data['borough'].str.strip()  \n",
    "energy_clean_textual_data['account_name'] = energy_clean_textual_data['account_name'].str.strip()  \n",
    "energy_clean_textual_data['funding_origin'] = energy_clean_textual_data['funding_origin'].str.strip() \n",
    "\n",
    "# Replace multiple spaces with a single space\n",
    "energy_clean_textual_data['borough'] = energy_clean_textual_data['borough'].str.replace(r'\\s+', ' ', regex=True)\n",
    "energy_clean_textual_data['account_name'] = energy_clean_textual_data['account_name'].str.replace(r'\\s+', ' ', regex=True)\n",
    "\n",
    "# Correct typos\n",
    "# spell = Speller(lang='en')\n",
    "# energy_clean_textual_data['borough'] = energy_clean_textual_data['borough'].apply(lambda x: spell(x))\n",
    "\n",
    "# Remove punctuation\n",
    "energy_clean_textual_data['borough'] = energy_clean_textual_data['borough'].str.replace(r'[^\\w\\s]', '', regex=True)\n",
    "energy_clean_textual_data['account_name'] = energy_clean_textual_data['account_name'].str.replace(r'[^\\w\\s]', '', regex=True)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Task 6: Remove Duplicates\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>2009-12-24</td>\n",
       "      <td>2010-01-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>2010-01-26</td>\n",
       "      <td>2010-02-25</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  borough account_name serial_number funding_origin  total_bill  \\\n",
       "0   bronx        adams       7223256        federal    15396.82   \n",
       "1   bronx        adams       7223256        federal    14556.34   \n",
       "\n",
       "   kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month start_date  \\\n",
       "0         128800.0    2808.0           216.0   2808.0 2010-01-01 2009-12-24   \n",
       "1         115200.0    2912.0           224.0   2912.0 2010-02-01 2010-01-26   \n",
       "\n",
       "    end_date  \n",
       "0 2010-01-26  \n",
       "1 2010-02-25  "
      ]
     },
     "execution_count": 56,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_remove_duplicate = energy_clean_textual_data.copy()\n",
    "energy_remove_duplicate.head(2)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Duplicate indicator for each row:\n",
      "Total number of duplicates: 16656\n"
     ]
    }
   ],
   "source": [
    "# Identify duplicates\n",
    "\n",
    "# dentify duplicates\n",
    "duplicates = energy_remove_duplicate.duplicated()  # Returns a boolean Series indicating duplicate rows\n",
    "print(\"Duplicate indicator for each row:\")\n",
    "\n",
    "# Determine the total number of duplicates\n",
    "total_duplicates = duplicates.sum()  # Sums the boolean Series to count duplicates\n",
    "print(\"Total number of duplicates:\", total_duplicates)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Duplicate rows:\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>102353</th>\n",
       "      <td>brooklyn</td>\n",
       "      <td>williamsburg</td>\n",
       "      <td>6484342</td>\n",
       "      <td>federal</td>\n",
       "      <td>2762.92</td>\n",
       "      <td>19360.0</td>\n",
       "      <td>1369.82</td>\n",
       "      <td>76.8</td>\n",
       "      <td>1369.82</td>\n",
       "      <td>2013-11-01</td>\n",
       "      <td>2013-10-23</td>\n",
       "      <td>2013-11-21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>102354</th>\n",
       "      <td>brooklyn</td>\n",
       "      <td>williamsburg</td>\n",
       "      <td>6484344</td>\n",
       "      <td>federal</td>\n",
       "      <td>2922.76</td>\n",
       "      <td>20480.0</td>\n",
       "      <td>941.75</td>\n",
       "      <td>52.8</td>\n",
       "      <td>941.75</td>\n",
       "      <td>2013-11-01</td>\n",
       "      <td>2013-10-23</td>\n",
       "      <td>2013-11-21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>102355</th>\n",
       "      <td>brooklyn</td>\n",
       "      <td>williamsburg</td>\n",
       "      <td>6484356</td>\n",
       "      <td>federal</td>\n",
       "      <td>5845.60</td>\n",
       "      <td>40960.0</td>\n",
       "      <td>1940.58</td>\n",
       "      <td>108.8</td>\n",
       "      <td>1940.58</td>\n",
       "      <td>2013-11-01</td>\n",
       "      <td>2013-10-23</td>\n",
       "      <td>2013-11-21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>102356</th>\n",
       "      <td>brooklyn</td>\n",
       "      <td>williamsburg</td>\n",
       "      <td>6484397</td>\n",
       "      <td>federal</td>\n",
       "      <td>913.32</td>\n",
       "      <td>6400.0</td>\n",
       "      <td>1112.98</td>\n",
       "      <td>62.4</td>\n",
       "      <td>1112.98</td>\n",
       "      <td>2013-11-01</td>\n",
       "      <td>2013-10-23</td>\n",
       "      <td>2013-11-21</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>102357</th>\n",
       "      <td>brooklyn</td>\n",
       "      <td>williamsburg</td>\n",
       "      <td>6484474</td>\n",
       "      <td>federal</td>\n",
       "      <td>5845.60</td>\n",
       "      <td>40960.0</td>\n",
       "      <td>1483.97</td>\n",
       "      <td>83.2</td>\n",
       "      <td>1483.97</td>\n",
       "      <td>2013-11-01</td>\n",
       "      <td>2013-10-23</td>\n",
       "      <td>2013-11-21</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "         borough  account_name serial_number funding_origin  total_bill  \\\n",
       "102353  brooklyn  williamsburg       6484342        federal     2762.92   \n",
       "102354  brooklyn  williamsburg       6484344        federal     2922.76   \n",
       "102355  brooklyn  williamsburg       6484356        federal     5845.60   \n",
       "102356  brooklyn  williamsburg       6484397        federal      913.32   \n",
       "102357  brooklyn  williamsburg       6484474        federal     5845.60   \n",
       "\n",
       "        kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month  \\\n",
       "102353          19360.0   1369.82            76.8  1369.82 2013-11-01   \n",
       "102354          20480.0    941.75            52.8   941.75 2013-11-01   \n",
       "102355          40960.0   1940.58           108.8  1940.58 2013-11-01   \n",
       "102356           6400.0   1112.98            62.4  1112.98 2013-11-01   \n",
       "102357          40960.0   1483.97            83.2  1483.97 2013-11-01   \n",
       "\n",
       "       start_date   end_date  \n",
       "102353 2013-10-23 2013-11-21  \n",
       "102354 2013-10-23 2013-11-21  \n",
       "102355 2013-10-23 2013-11-21  \n",
       "102356 2013-10-23 2013-11-21  \n",
       "102357 2013-10-23 2013-11-21  "
      ]
     },
     "execution_count": 58,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Step 2: Display duplicate rows\n",
    "duplicate_rows = energy_remove_duplicate[energy_remove_duplicate.duplicated()]  # Extracts duplicate rows\n",
    "print(\"Duplicate rows:\")\n",
    "duplicate_rows.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Save to clean data \n",
    "energy_clean = energy_clean_textual_data.copy()\n",
    "energy_clean.to_csv(\"energy_remove_\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Data vi.... and insight"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "metadata": {},
   "outputs": [
    {
     "ename": "AttributeError",
     "evalue": "module 'pandas' has no attribute 'read'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mAttributeError\u001b[0m                            Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[60], line 2\u001b[0m\n\u001b[1;32m      1\u001b[0m \u001b[38;5;66;03m# path clean\u001b[39;00m\n\u001b[0;32m----> 2\u001b[0m energy_clean \u001b[38;5;241m=\u001b[39m \u001b[43mpd\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mread\u001b[49m(\u001b[38;5;124m'\u001b[39m\u001b[38;5;124m'\u001b[39m)\n",
      "\u001b[0;31mAttributeError\u001b[0m: module 'pandas' has no attribute 'read'"
     ]
    }
   ],
   "source": [
    "# path clean\n",
    "energy_clean = pd.read('')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "Index(['borough', 'account_name', 'serial_number', 'funding_origin',\n",
       "       'total_bill', 'kwh_consumption', 'kwh_bill', 'kw_consumption',\n",
       "       'kw_bill', 'year_month', 'start_date', 'end_date'],\n",
       "      dtype='object')"
      ]
     },
     "execution_count": 61,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_clean_textual_data.columns"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Plot a line graph of kWh (kilowatt-hour) usage against billing dates"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "metadata": {},
   "outputs": [],
   "source": [
    "energy_ymth_kwh = (energy_clean_textual_data\n",
    "    .groupby(['year_month'])['kwh_consumption'].sum()\n",
    "    .reset_index())"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>year_month</th>\n",
       "      <th>kwh_consumption</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>106298266.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>93139547.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2010-03-01</td>\n",
       "      <td>88477980.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>2010-04-01</td>\n",
       "      <td>89076605.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2010-05-01</td>\n",
       "      <td>89637927.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  year_month  kwh_consumption\n",
       "0 2010-01-01      106298266.0\n",
       "1 2010-02-01       93139547.0\n",
       "2 2010-03-01       88477980.0\n",
       "3 2010-04-01       89076605.0\n",
       "4 2010-05-01       89637927.0"
      ]
     },
     "execution_count": 63,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_ymth_kwh.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAA04AAAIjCAYAAAA0vUuxAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8fJSN1AAAACXBIWXMAAA9hAAAPYQGoP6dpAADmhElEQVR4nOydd3wUZf7HP7Ob3uglkFAUVFBAFFSadJUgIhEbeiqe53kWQDz18E7FXs4C3uk1/Yl6iAUj6hlF1FBFBTWKYkEMLYQeEkLaZnd+fzw+O7ObLVOe3Z2Z/b5fr7x2Mzu7+8w+M888n+fbJFmWZRAEQRAEQRAEQRBhcSW6AQRBEARBEARBEFaHhBNBEARBEARBEEQUSDgRBEEQBEEQBEFEgYQTQRAEQRAEQRBEFEg4EQRBEARBEARBRIGEE0EQBEEQBEEQRBRIOBEEQRAEQRAEQUSBhBNBEARBEARBEEQUSDgRBEEQBEEQBEFEgYQTQRCEBubPnw9JknDgwIGYfs/KlSshSRKWLl0a0+8hIrNt2zZIkoRFixYluim2h187BEEQdoeEE0EQhCCuv/56uFwuHDp0KGD7oUOH4HK5kJ6ejsbGxoDXfvnlF0iShDvuuCOeTSV+5eWXX8aCBQsS3Qzb0atXL0iSFPWPhCdBEE4iJdENIAiCcAojR47EP/7xD6xbtw5Tpkzxb//kk0/gcrng8XiwceNGjBw50v/aunXr/O8l4s/LL7+Mb7/9FnPmzAnY3rNnTzQ0NCA1NTUxDbM4CxYsQF1dnf//0tJSLFmyBE8++SQ6duzo3z58+HBcfvnl+NOf/pSIZhIEQQiFhBNBEIQguPhZu3ZtgHBat24dBg4ciIaGBqxduzZAJK1duxYulwvDhw+Pe3uJ8EiShIyMjEQ3I+EcPXoU2dnZrbaff/75Af/v2bMHS5Yswfnnn49evXq12j8lhaYbBEHYH3LVIwiCMMj27dvRp08fnHTSSdi7dy969OiBwsJCvxWJs27dOowYMQLDhw8P+dqJJ56Itm3bBmz3+Xx44IEHUFBQgIyMDIwfPx4///yzpnZVVlbit7/9Lbp164b09HT07t0bf/jDH9Dc3Ozf55dffsGFF16I9u3bIysrC2eccQbefffdgM/h8VavvfZa1LZs2bIFF1xwAbp27YqMjAwUFBTgkksuQU1NDYDIMUOSJGH+/Pn+/3lMzE8//YTLL78cbdq0QadOnXDnnXdClmXs3LkTU6dORV5eHrp27YrHH388ZLtfffVV3HHHHejatSuys7Nx3nnnYefOnf79xowZg3fffRfbt2/3u5bxSX+49n788ccYNWoUsrOz0bZtW0ydOhXff/99wD68/T///DOuuuoqtG3bFm3atMHMmTNRX18fse84r7/+Ok499VRkZmaiY8eOuPzyy1FZWel//bHHHoMkSdi+fXur986bNw9paWmorq72b/vss89wzjnnoE2bNsjKysLo0aNbnYu83Zs3b8aMGTPQrl07IZbQUDFOkiThxhtvxOuvv47+/fsjMzMTw4YNw6ZNmwAA//rXv9CnTx9kZGRgzJgx2LZtW6vP1XJMBEEQIqElIIIgCANs3boV48aNQ/v27bFixQq/e9LIkSNRUlKCpqYmpKeno7m5GRs2bMAf/vAH1NfX47bbboMsy5AkCdXV1di8eTOuu+66Vp//8MMPw+Vy4Y9//CNqamrw6KOP4rLLLsNnn30WsV27d+/GaaedhsOHD+Paa6/FCSecgMrKSixduhT19fVIS0vD3r17MXz4cNTX12PWrFno0KEDXnjhBZx33nlYunQppk2bpqstzc3NOPvss9HU1ISbbroJXbt2RWVlJf73v//h8OHDaNOmjaHf+OKLL0a/fv3w8MMP491338X999+P9u3b41//+hfGjRuHRx55BIsXL8Yf//hHDB06FGeeeWbA+x944AFIkoTbb78d+/btw4IFCzBhwgSUl5cjMzMTf/7zn1FTU4Ndu3bhySefBADk5OSEbc+HH36ISZMm4ZhjjsH8+fPR0NCAv/3tbxgxYgS+/PLLVpaWiy66CL1798ZDDz2EL7/8Es8++yw6d+6MRx55JOJxL1q0CDNnzsTQoUPx0EMPYe/evVi4cCHWrVuHr776Cm3btsVFF12E2267Da+99hpuvfXWgPe/9tprOOuss9CuXTsATOxNmjQJp556Ku6++264XC48//zzGDduHNasWYPTTjst4P0XXngh+vbtiwcffBCyLEdsqxnWrFmDt99+GzfccAMA4KGHHsK5556L2267Dc888wyuv/56VFdX49FHH8XVV1+Njz/+2P9evcdEEAQhBJkgCIKIyt133y0DkPfv3y9///33crdu3eShQ4fKhw4dCtjv6aeflgHIa9askWVZltevXy8DkLdv3y5v3rxZBiB/9913sizL8v/+9z8ZgLx48WL/+8vKymQAcr9+/eSmpib/9oULF8oA5E2bNkVs5xVXXCG7XC55w4YNrV7z+XyyLMvynDlzAtooy7J85MgRuXfv3nKvXr1kr9erqy1fffWVDEB+/fXXw7aroqJCBiA///zzrV4DIN99993+//lvfe211/q3tbS0yAUFBbIkSfLDDz/s315dXS1nZmbKV155pX8bb3f37t3l2tpa//bXXntNBiAvXLjQv23y5Mlyz549NbX35JNPljt37iwfPHjQv+3rr7+WXS6XfMUVV7Rq/9VXXx3wmdOmTZM7dOgQ8vfhNDc3y507d5ZPOukkuaGhwb+dnyt33XWXf9uwYcPkU089NeD9n3/+uQxAfvHFF2VZZn3et29f+eyzz/b3vyzLcn19vdy7d2954sSJrdp96aWXRmxjKP7617/KAOSKiopWr/HPVQNATk9PD9j/X//6lwxA7tq1a0C/zZs3L+Cz9RwTQRCESMhVjyAIQgfffvstRo8ejV69euHDDz/0r+pz1HFOAHPF6969O3r06IETTjgB7du397sTRUoMMXPmTKSlpfn/HzVqFADmYhcOn8+HZcuWYcqUKRgyZEir17m7VGlpKU477bSA783JycG1116Lbdu2YfPmzbrawi1Ky5cv1+yKpoVrrrnG/9ztdmPIkCGQZRm//e1v/dvbtm2L448/PuTvcsUVVyA3N9f///Tp05Gfn4/S0lLdbamqqkJ5eTmuuuoqtG/f3r994MCBmDhxYsjPDLYkjho1CgcPHkRtbW3Y79m4cSP27duH66+/PiDGavLkyTjhhBMC3CkvvvhifPHFF9i6dat/26uvvor09HRMnToVAFBeXo4tW7ZgxowZOHjwIA4cOIADBw7g6NGjGD9+PFavXg2fzxex3bFi/PjxAVa6008/HQBwwQUXBPQb38772MgxEQRBiCCphdPq1asxZcoUdOvWDZIkYdmyZbo/Y/ny5TjjjDOQm5uLTp064YILLgjpi00QhDOYMmUKcnNzsXz5cuTl5bV6/aSTTkLbtm0DxNGIESMAMOEybNiwgNcKCwvRo0ePVp8TvI0LNHXcSjD79+9HbW0tTjrppIjHsH37dhx//PGttvfr18//up629O7dG3PnzsWzzz6Ljh074uyzz8bTTz/tj28ySvD3tmnTBhkZGQFZ2/j2UL9L3759A/6XJAl9+vQxNEbz3yTc78Yn7pHar6UPI33PCSecENA3F154IVwuF1599VUAgCzLeP311zFp0iT/ubllyxYAwJVXXolOnToF/D377LNoampq1U+9e/cO2z6RhOpfACgsLAy5nf9uRo6JIAhCBEktnI4ePYpBgwbh6aefNvT+iooKTJ06FePGjUN5eTmWL1+OAwcOoLi4WHBLCYKwChdccAG2bt2KxYsXh3zd5XJh2LBh+OSTTyDLMtatWxeQMW/48OFYu3atP/YpXPC92+0OuV2OYcxJOLS05fHHH8c333yDO+64Aw0NDZg1axZOPPFE7Nq1CwDCFkD1er26vtdKv0s0Yt3Wbt26YdSoUXjttdcAAJ9++il27NiBiy++2L8Pt7z89a9/xYoVK0L+Bcd1ZWZmCmlfNML9PtF+NyPHRBAEIYKkTg4xadIkTJo0KezrTU1N+POf/4wlS5bg8OHDOOmkk/DII49gzJgxAIAvvvgCXq8X999/P1wupkH/+Mc/YurUqfB4PFT/gyAcyF//+lekpKTg+uuvR25uLmbMmNFqn5EjR+K9997D22+/jX379vktTgATTn/+859RWlqKhoYGofWbOnXqhLy8PHz77bcR9+vZsyd+/PHHVtt/+OEH/+tGGDBgAAYMGIC//OUv+OSTTzBixAj885//xP333++3thw+fDjgPaGywomCWyY4sizj559/xsCBA/3bwgm6YPhvEu5369ixY8i03XpRf8+4ceMCXvvxxx9b9c3FF1+M66+/Hj/++CNeffVVZGVlBaTCP/bYYwEAeXl5mDBhgun2WQEnHhNBEPYgqS1O0bjxxhuxfv16vPLKK/jmm29w4YUX4pxzzvHfjE899VR/Jh+v14uamhq89NJLmDBhAokmgnAokiTh3//+N6ZPn44rr7wSb7/9dqt9uBh65JFHkJWVhZNPPtn/2mmnnYaUlBQ8+uijAfuKwOVy4fzzz8c777yDjRs3tnqdr9gXFRXh888/x/r16/2vHT16FP/+97/Rq1cv9O/fX9f31tbWoqWlJWDbgAED4HK50NTUBIBNcjt27IjVq1cH7PfMM8/o+i49vPjiizhy5Ij//6VLl6KqqipgwSw7O1uTW1d+fj5OPvlkvPDCCwHi79tvv8UHH3yAoqIiIW0eMmQIOnfujH/+85/+3w4A3nvvPXz//feYPHlywP4XXHAB3G43lixZgtdffx3nnntugIA79dRTceyxx+Kxxx4LKFjL2b9/v5B2xxMnHhNBEPYgqS1OkdixYweef/557NixA926dQPArEnvv/8+nn/+eTz44IPo3bs3PvjgA1x00UX4/e9/D6/Xi2HDhhkKPCYIwj64XC7897//xfnnn4+LLroIpaWlAdaB0047DWlpaVi/fj3GjBkTUPwzKysLgwYNwvr169G2bduo8Uh6efDBB/HBBx9g9OjRuPbaa9GvXz9UVVXh9ddfx9q1a9G2bVv86U9/wpIlSzBp0iTMmjUL7du3xwsvvICKigq88cYbfgu6Vj7++GPceOONuPDCC3HcccehpaUFL730EtxuNy644AL/ftdccw0efvhhXHPNNRgyZAhWr16Nn376Sejxq2nfvj1GjhyJmTNnYu/evViwYAH69OmD3/3ud/59Tj31VLz66quYO3cuhg4dipycnACLjZq//vWvmDRpEoYNG4bf/va3/nTkbdq0CahDZYbU1FQ88sgjmDlzJkaPHo1LL73Un468V69euPnmmwP279y5M8aOHYsnnngCR44cCXDTA9i5+uyzz2LSpEk48cQTMXPmTHTv3h2VlZUoKytDXl4e3nnnHSFtjxdOPCaCIOwBCacwbNq0CV6vF8cdd1zA9qamJnTo0AEAq5T+u9/9DldeeSUuvfRSHDlyBHfddRemT5+OFStWaHYBIQjCfqSmpmLp0qWYNGkSpk6dig8//NCf/SsjIwOnnnoq1q9fHxDfxBkxYgS++OILDBs2TLdIiUb37t3x2Wef4c4778TixYtRW1uL7t27Y9KkScjKygIAdOnSBZ988gluv/12/O1vf0NjYyMGDhyId955p5VFQwuDBg3C2WefjXfeeQeVlZV+cfjee+/hjDPO8O931113Yf/+/Vi6dClee+01TJo0Ce+99x46d+4s7PjV3HHHHfjmm2/w0EMP4ciRIxg/fjyeeeYZ/+8AANdffz3Ky8vx/PPP48knn0TPnj3DCqcJEybg/fffx91334277roLqampGD16NB555BGhCRWuuuoqZGVl4eGHH8btt9+O7OxsTJs2DY888kirQskAc9f78MMPkZubG9LyNWbMGKxfvx733Xcf/v73v6Ourg5du3bF6aefjt///vfC2h1PnHhMBEFYH0m2YkRt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IiLHMXAiIiK30+l0CAoKws2bN93yfC1atEB5eTn27t2LDh06ABDZnsuXLzu1vSNHjuDbb7/F1KlTjfcvXbqEd955BwkJCQCA3bt3WzwmNDQUAFBRUWFc1rp1axgMBuTn57NbHhGRl2PgREREmispKcG5c+cAAJcvX8b8+fNx7do1pKSkuOX5W7ZsiZ49e2LcuHH46KOPEBISgj/96U8ICwuz6G5nTXl5Oc6dO4fKykpcunQJOTk5mDVrFtq1a4c///nPAIBGjRohNDQU//znPzF+/HgcOHAAb775psV2GjduDJ1Oh3Xr1uHhhx9GWFgYIiIi8PLLL2PSpEmorKxE165dUVRUhK1btyIyMhIjRozQ7H9CRESO4RgnIiLS3Lfffou4uDjExcWhc+fO2LVrF9LT0/HAAw+4bR+WLl2KmJgYdO/eHQMGDMDYsWMRERGBWrVq2XzcwYMHERcXh0aNGuGBBx7AmjVrMHXqVGzZssVY8CI6OhppaWlIT09H69at8c4772DOnDkW22nYsCFmzpyJV155BTExMXjhhRcAAG+++SZef/11zJ49G61atULfvn3xzTffGLsBEhGRd9BJkiR5eieIiIjc7cyZM0hISMDGjRvx4IMPenp3iIjIyzFwIiKigLBp0yZcu3YNd911FwoLCzFlyhQUFBTgp59+qlZYgoiIqCqOcSIiooBQVlaGV199FSdOnEBERAS6dOmC5cuXM2giIiJFmHEiIiIiIiKyg8UhiIiIiIiI7GDgREREREREZAcDJyIiIiIiIjsYOBEREREREdnBwImIiIiIiMgOBk5ERERERER2MHAiIiIiIiKyg4ETERERERGRHf8PCGhybFPfCjgAAAAASUVORK5CYII=",
      "text/plain": [
       "<Figure size 1000x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Plot\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.plot(energy_ymth_kwh['year_month'], energy_ymth_kwh['kwh_consumption'], marker='o', linestyle='-', color='b', label='kWh consumption')\n",
    "\n",
    "plt.title('kWh consumption over Time')\n",
    "plt.xlabel('Billing Date')\n",
    "plt.ylabel('kWh_consumption')\n",
    "plt.grid(True)\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 100,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>year_month</th>\n",
       "      <th>kwh_consumption</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>106298266.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>93139547.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2010-03-01</td>\n",
       "      <td>88477980.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>2010-04-01</td>\n",
       "      <td>89076605.0</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>2010-05-01</td>\n",
       "      <td>89637927.0</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  year_month  kwh_consumption\n",
       "0 2010-01-01      106298266.0\n",
       "1 2010-02-01       93139547.0\n",
       "2 2010-03-01       88477980.0\n",
       "3 2010-04-01       89076605.0\n",
       "4 2010-05-01       89637927.0"
      ]
     },
     "execution_count": 100,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 106,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAABAcAAAIjCAYAAAB/KXJYAAAAOXRFWHRTb2Z0d2FyZQBNYXRwbG90bGliIHZlcnNpb24zLjguNCwgaHR0cHM6Ly9tYXRwbG90bGliLm9yZy8fJSN1AAAACXBIWXMAAA9hAAAPYQGoP6dpAAB23UlEQVR4nO3dd3QUZf/+8WsTSCEhIbSE0IL09oCAQOglD6FIUVCaUkRQJHQRbBRRURQp0gR9ABUEUQSM0qQKhCrdEIpIEQIqJCGhBJL79wffzI8lARJIAfb9OifnZGbumfnM7Mwme+3MPTZjjBEAAAAAAHBYTlldAAAAAAAAyFqEAwAAAAAAODjCAQAAAAAAHBzhAAAAAAAADo5wAAAAAAAAB0c4AAAAAACAgyMcAAAAAADAwREOAAAAAADg4AgHAAAAAABwcIQDAIBMY7PZNHLkyKwu47599dVXKlOmjLJnz65cuXLdtl23bt3k6emZ4fXMnj1bNptNO3bsyPB1IXUCAgLUrVu3rC4Dj5AGDRqoQoUKWV0GgEcY4QAAZKKjR4/qpZde0mOPPSY3Nzd5eXmpdu3amjhxoi5fvpzV5SEVDh48qG7duql48eKaOXOmZsyYcV/La968uXx8fGSMsRu/a9cu2Ww2FS1aNNk8a9askc1mu+9132r37t167rnnVLhwYbm6uip37twKCgrSrFmzlJCQkK7rehRs3rxZI0eOVFRUVFaXkqKpU6fKZrOpRo0aWV1KhmnQoIFsNpv14+LiomLFiqlXr146efJkVpcHAA+VbFldAAA4ip9++knPPPOMXF1d1aVLF1WoUEHx8fHauHGjhgwZogMHDqT7h70HzeXLl5Ut28P9p2fdunVKTEzUxIkTVaJEifteXp06dbRs2TLt379fFStWtMZv2rRJ2bJl04kTJ3Tq1CkVKlTIblrSvOnl888/18svvyxfX189//zzKlmypC5evKjVq1erR48eOnPmjN544410W9+jYPPmzRo1apS6deuW7AqSiIgIOTll7Xcwc+fOVUBAgLZt26YjR46ky/H6ICpUqJDGjBkjSYqPj9fvv/+u6dOna8WKFQoPD1eOHDmyuEIAeDg83P+hAcBD4tixY+rQoYOKFi2qNWvWqECBAta0Pn366MiRI/rpp5+ysMKMk5iYqPj4eLm5ucnNzS2ry7lv586dk6Q73k6QFkkf8Ddu3JgsHGjevLnWrFmjjRs3qkOHDta0jRs3Kk+ePCpbtmy61LBlyxa9/PLLCgwM1M8//6ycOXNa0wYMGKAdO3Zo//796bIuR+Hq6pql6z927Jg2b96sRYsW6aWXXtLcuXM1YsSIdFn2lStX5OLikuXhRxJvb28999xzduOKFSumkJAQbdq0Sf/973/vex1xcXHy8PC47+UAwIPswXhXB4BH3NixYxUbG6svvvjCLhhIUqJECfXv398avn79ukaPHq3ixYvL1dVVAQEBeuONN3T16lW7+QICAvTkk09q3bp1qlatmtzd3VWxYkWtW7dOkrRo0SJVrFhRbm5uqlq1qnbt2mU3f9I98X/88YeCg4Pl4eEhf39/vfPOO8kuc//4449Vq1Yt5cmTR+7u7qpataq+++67ZNtis9kUEhKiuXPnqnz58nJ1ddXy5cutaTf3OXDx4kUNGDBAAQEBcnV1Vf78+fXf//5Xv/32m90yFy5cqKpVq8rd3V158+bVc889p7/++ivFbfnrr7/Upk0beXp6Kl++fHr11VdTfUn81KlTrZr9/f3Vp08fu0vGAwICrA9Y+fLlu6c+FHbv3q18+fKpQYMGio2NVfXq1eXi4mJdDZBk06ZNqlevnqpXr243LTExUVu2bFGtWrVks9ns5rl69aoGDRqkfPnyycPDQ0899ZT+/vvvu9Y0atQo2Ww2zZ071y4YSFKtWjW7++fj4uI0ePBg6/aD0qVL6+OPP052zCQdC4sXL1aFChXk6uqq8uXLW8dDktQcB7e7h79BgwZq0KCBNbxu3TrZbDZ9++23GjVqlAoWLKicOXOqXbt2io6O1tWrVzVgwADlz59fnp6e6t69e7Lz6uZjuHTp0tb5s2HDBqvNyJEjNWTIEEk3PogmXdb+559/3rbeP/74Q88884xy586tHDlyqGbNmslCwZvrf++991SoUCG5ubmpcePGOnLkSLLtv525c+fKx8dHLVq0ULt27TR37twU20VFRWngwIHWvi9UqJC6dOmif/75x66e+fPn66233lLBggWVI0cOxcTESErduRkZGanu3burUKFCcnV1VYECBdS6dWtrX0nSjh07FBwcrLx588rd3V3FihXTCy+8kOrtvZWfn58kJbtSadeuXWrWrJm8vLzk6empxo0ba8uWLXZtkvrwWL9+vV555RXlz5/f7sqdu71PSKk/XiXp+PHjatWqlTw8PJQ/f34NHDhQK1askM1ms97Lb/b777+rYcOGypEjhwoWLKixY8cma/Ppp5+qfPnyypEjh3x8fFStWjXNmzfvDnsMALhyAAAyxY8//qjHHntMtWrVSlX7F198UXPmzFG7du00ePBgbd26VWPGjFF4eLh++OEHu7ZHjhxRp06d9NJLL+m5557Txx9/rJYtW2r69Ol644039Morr0iSxowZo2effTbZ5c4JCQlq2rSpatasqbFjx2r58uUaMWKErl+/rnfeecdqN3HiRLVq1UqdO3dWfHy85s+fr2eeeUahoaFq0aKFXU1r1qzRt99+q5CQEOXNm1cBAQEpbufLL7+s7777TiEhISpXrpz+/fdfbdy4UeHh4apSpYqkG/+od+/eXU888YTGjBmjs2fPauLEidq0aZN27dpl9w1+QkKCgoODVaNGDX388cf65ZdfNG7cOBUvXly9e/e+4z4fOXKkRo0apaCgIPXu3VsRERGaNm2atm/frk2bNil79uyaMGGCvvzyS/3www+aNm2aPD099Z///Oeur2eS7du3Kzg4WNWqVdOSJUvk7u4uSapatao2btxotTt58qROnjypWrVqKSoqyu4D5L59+xQTE5PiLQV9+/aVj4+PRowYoT///FMTJkxQSEiIFixYcNuaLl26pNWrV6tevXoqUqTIXbfBGKNWrVpp7dq16tGjhypXrqwVK1ZoyJAh+uuvvzR+/Hi79hs3btSiRYv0yiuvKGfOnJo0aZLatm2rEydOKE+ePJJSdxyk1ZgxY+Tu7q5hw4bpyJEj+vTTT5U9e3Y5OTnpwoULGjlypLZs2aLZs2erWLFiGj58uN3869ev14IFC9SvXz+5urpq6tSpatq0qbZt26YKFSro6aef1qFDh/TNN99o/Pjxyps3r6QboVFKzp49q1q1aunSpUvq16+f8uTJozlz5qhVq1b67rvv9NRTT9m1/+CDD+Tk5KRXX31V0dHRGjt2rDp37qytW7emavvnzp2rp59+Wi4uLurYsaN1LD/xxBNWm9jYWNWtW1fh4eF64YUXVKVKFf3zzz9aunSpTp06ZW2TJI0ePVouLi569dVXdfXqVbm4uKT63Gzbtq0OHDigvn37KiAgQOfOndOqVat04sQJa7hJkybKly+fhg0bply5cunPP//UokWLUrWtCQkJVphx7do1hYeHa8SIESpRooRq165ttTtw4IDq1q0rLy8vvfbaa8qePbs+++wzNWjQQOvXr0/WN8Mrr7yifPnyafjw4YqLi5OUuveJtIiLi1OjRo105swZ9e/fX35+fpo3b57Wrl2bYvsLFy6oadOmevrpp/Xss8/qu+++09ChQ1WxYkU1a9ZMkjRz5kz169dP7dq1U//+/XXlyhXt3btXW7duVadOndJUHwAHYwAAGSo6OtpIMq1bt05V+927dxtJ5sUXX7Qb/+qrrxpJZs2aNda4okWLGklm8+bN1rgVK1YYScbd3d0cP37cGv/ZZ58ZSWbt2rXWuK5duxpJpm/fvta4xMRE06JFC+Pi4mL+/vtva/ylS5fs6omPjzcVKlQwjRo1shsvyTg5OZkDBw4k2zZJZsSIEdawt7e36dOnz233RXx8vMmfP7+pUKGCuXz5sjU+NDTUSDLDhw9Pti3vvPOO3TIef/xxU7Vq1duuwxhjzp07Z1xcXEyTJk1MQkKCNX7y5MlGkvnf//5njRsxYoSRZLdvbqdr167Gw8PDGGPMxo0bjZeXl2nRooW5cuWKXbshQ4YYSebUqVPGGGO++eYb4+bmZq5evWp+/vln4+zsbGJiYuxq2rRpkzX/rFmzjCQTFBRkEhMTrfEDBw40zs7OJioq6rY17tmzx0gy/fv3v+v2GGPM4sWLjSTz7rvv2o1v166dsdls5siRI9Y4ScbFxcVuXNL6Pv30U2vc3Y4DY24c6127dk02vn79+qZ+/frW8Nq1a40kU6FCBRMfH2+N79ixo7HZbKZZs2Z28wcGBpqiRYvajZNkJJkdO3ZY444fP27c3NzMU089ZY376KOPjCRz7Nixu9Y7YMAAI8n8+uuv1riLFy+aYsWKmYCAAOu4S6q/bNmy5urVq1bbiRMnGklm3759Ke6fm+3YscNIMqtWrTLG3DinCxUqlOw1Hj58uJFkFi1alGwZScdRUj2PPfaY3XtAas/NCxcuGEnmo48+um29P/zwg5Fktm/fftdtu1X9+vWt1+vmn7Jly5o//vjDrm2bNm2Mi4uLOXr0qDXu9OnTJmfOnKZevXrWuKTzqU6dOub69evW+LS8T6T2eB03bpyRZBYvXmyNu3z5silTpkyy9+ukbf3yyy+tcVevXjV+fn6mbdu21rjWrVub8uXL32XPAUBy3FYAABks6fLblC7XTsnPP/8sSRo0aJDd+MGDB0tSssuQy5Urp8DAQGs46duvRo0a2X0TnDT+jz/+SLbOkJAQ6/ekS6rj4+P1yy+/WOOTvuWWbnx7FR0drbp16ya7BUCS6tevr3Llyt1lS2/ct79161adPn06xek7duzQuXPn9Morr9j1V9CiRQuVKVMmxX4aXn75ZbvhunXrprjNN/vll18UHx+vAQMG2F1V0bNnT3l5ed13fxBr165VcHCwGjdurEWLFiW7Hz3pKoBff/1V0o1bCqpWrSoXFxcFBgZatxIkTXNzc1O1atWSradXr152txrUrVtXCQkJOn78+G1ru5fj09nZWf369bMbP3jwYBljtGzZMrvxQUFBKl68uDX8n//8R15eXnavyd2Og3vRpUsXu29xa9SoIWNMskvVa9SooZMnT+r69et24wMDA1W1alVruEiRImrdurVWrFhxT09u+Pnnn1W9enW7Kz48PT3Vq1cv/fnnn/r999/t2nfv3l0uLi7WcN26dSWlfP7eau7cufL19VXDhg0l3Tin27dvr/nz59vV/v3336tSpUrJrlpImudmXbt2tXsPSO256e7uLhcXF61bt04XLlxIsd6kKwxCQ0N17dq1u27frQICArRq1SqtWrVKy5Yt04QJExQdHa1mzZpZt9UkJCRo5cqVatOmjR577DFr3gIFCqhTp07auHGjdS4k6dmzp5ydna3hjHifWL58uQoWLKhWrVpZ49zc3NSzZ88U23t6etr1r+Di4qLq1asnO59OnTql7du3p7keAI6NcAAAMpiXl5ekG/dVp8bx48fl5OSUrGdxPz8/5cqVK9kHvVsvBff29pYkFS5cOMXxt/6D7uTkZPfPsiSVKlVKkuzuCQ4NDVXNmjXl5uam3LlzK1++fJo2bZqio6OTbUOxYsXutpmSbvTFsH//fhUuXFjVq1fXyJEj7f7JTdrW0qVLJ5u3TJkyyfaFm5tbssu6fXx8bvuh5G7rcXFx0WOPPXbHD9d3c+XKFbVo0UKPP/64vv32W7sPfElq164tm81m9S2wadMm63LoXLlyqVy5cnbTnnjiiRSXc+ux4OPjIyn5a36zezk+/f39k4UJSZ0j3u34TKrr5prudhzci7ScF4mJicmO45IlSyZbZqlSpXTp0qVU9eNwq+PHj6d4HKd2v6XmtZRufAieP3++GjZsqGPHjunI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999/b/744w/z/fffm9y5c5vZs2cbY1J33rdo0cL897//NXv37jVHjx41P/74o1m/fn2m7KMH2enTp022bNnMJ598Yo4dO2b27t1rpkyZYi5evGguXrxonn32WdO0aVPrXEt6Te7lHDXGmKCgINOyZUuzfft2c+jQITN48GCTJ08e8++//xpjjBkxYoTx9PQ0Tz/9tNm3b5/ZsGGD8fPzM2+88cZtt+HmvyPGGFO+fHnz3HPPmfDwcHPo0CHz7bffmt27d6fYNj3eHy5evGjy5ctnOnXqZPbv329+/PFH89hjjxlJZteuXXa11q9f33h5eZmRI0eaQ4cOmTlz5hibzWZWrlxpjDEmISHBVK5c2dSpU8fs2LHDbNmyxVStWtXUr1/fWsa97KMtW7YYJycn8+GHH5qIiAgzceJEkytXLrt9sWHDBuPl5WVmz55tjh49alauXGkCAgLMyJEjjTHGhIaGGnd3d3Px4kVrnh9//NG4u7ubmJgYY4wx7777rilTpoxZvny5OXr0qJk1a5ZxdXU169atM8Yk/5ue2v8Xc+bMacaMGWMiIiLMpEmTjLOzs7XPjLnxPlOwYEGzYMECExERYdq0aWMCAgJMo0aNzPLly83vv/9uatasaZo2bZrq7U1abqFChcy8efPM4cOHTb9+/Yynp6f5999/zfXr1833339vJJmIiAhz5swZExUVlWzfX7161URERBhJ5vvvv7fOo1OnTpmPPvrI7Nq1yxw9etTarq1bt1rzvvbaa8bHx8fMnj3bHDlyxPz6669m5syZxpj//76XdIzdum9vPtZvd05u2rTJODs7m9OnT1vrXLRokfHw8LB7nR8UUVFR5p133jGFChWy/s7f7Zwyxpjx48ebNWvWmGPHjpnVq1eb0qVLm969e2fhljxYCAeQJvXr1zdly5Y1iYmJ1rihQ4easmXLGmNuvGm3adPGbp5OnTqZ//73v3bjhgwZYsqVK2cNFy1a1Dz33HPWcGJiosmfP7+ZNm2aNe78+fOmUKFCpnfv3sbX19e899576bpt+P8y4nU+dOiQkWQ2bdpkTf/nn3+Mu7u7+fbbb40x//+P18GDB03hwoVNv3797Gq49Y/d1q1b7f6QnT171mTLls36xyPpj+Xnn39uLePAgQNGkgkPD7+vffSoqV+/vqlTp441fP36dePh4WGef/55a9yZM2eM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m1SqVKnbzpOSzZs368MPP9SPP/6ooUOHKiQkxPrGGOkvvV/nsmXL6vr169q6davVq+y///6riIgIlStXzprHyclJX331lTp16qSGDRtq3bp1d+zN97nnntNrr72mSZMm6ffff1fXrl3vdZORBps2bVKtWrX0yiuvWOPu9I3cvdq8ebOKFi2qN9980xp3/PhxuzYuLi523yolyZ49e7LxmzZtUrdu3awPBrGxsck6u8O9KV68uLJnz66tW7eqSJEikm50Qnro0CHVr19f0o0P+GfOnLHmOXz4sN23NVWqVNGCBQuUP39+eXl5JVuHt7e3/P399ccff1jfUN6rwoUL6+WXX9bLL7+s119/XTNnznT4cEC68Y907dq1Vbt2bQ0fPlxFixbVDz/8oEGDBqV4rt3rOVqlShVFRkYqW7ZsVkdiGaVUqVIqVaqUBg4cqI4dO2rWrFkphgPp8f5QtmxZffXVV7py5Yr1oXLLli33VHfZsmV18uRJnTx50rp64Pfff1dUVJTd3817WW5Kf+NvVqVKFUVERKhEiRK3XU6tWrVUuHBhLViwQMuWLdMzzzxjfTArV66cXF1ddeLECev8T01dqfl/8dZat2zZorJly6ZqHbeTmu29m6SnNqX09+huNm3apNatW+u5556TdCO0OHTokPU6lyxZUu7u7lq9erVefPHFe67x5lpTqjNPnjxq06aNZs2apbCwMHXv3v2+1/Ug2blzpxITEzVu3Dg5Od24gP7bb7/N4qoeLNxWgDQ7ceKEBg0apIiICH3zzTf69NNP1b9//9u2Hzx4sFavXq3Ro0fr0KFDmjNnjiZPnqxXX3011eu8ePGinn/+efXr10/NmjXT3LlztWDBgrv2eot7l96vc8mSJdW6dWv17NlTGzdu1J49e/Tcc8+pYMGCat26td2ynJ2dNXfuXFWqVEmNGjVSZGTkbdfr4+Ojp59+WkOGDFGTJk1UqFCh9NkBuKOSJUtqx44dWrFihQ4dOqS3335b27dvz5D1nDhxQvPnz9fRo0c1adIk/fDDD3ZtAgICdOzYMe3evVv//POP9WSLgIAArV69WpGRkdal0SVLltSiRYu0e/du7dmzR506deKKgHTi6empHj16aMiQIVqzZo3279+vbt26Wf+ASTd65548ebJ27dqlHTt26OWXX7b7lqdz587KmzevWrdurV9//VXHjh3TunXr1K9fP506dUqSNGrUKI0ZM0aTJk3SoUOHtG/fPs2aNUuffPJJqmsdMGCAVqxYoWPHjum3337T2rVr7/vDxaNg69atev/997Vjxw6dOHFCixYt0t9//23tm4CAAO3du1cRERH6559/dO3atXs+R4OCghQYGKg2bdpo5cqV+vPPP7V582a9+eabt32aQFpdvnxZISEhWrdunY4fP65NmzZp+/btt32t0+P9oVOnTrLZbOrZs6d+//13/fzzz/r444/vqf6goCBVrFhRnTt31m+//aZt27apS5cuql+/frJb+9KiX79+Wr58uT7++GMdPnxYkydP1vLly+3aDB8+XF9++aVGjRqlAwcOKDw8XPPnz9dbb72VbHunT5+uVatW2QV2OXPm1KuvvqqBAwdqzpw5Onr0qH777Td9+umnt/1iJ7X/L27atEljx47VoUOHNGXKFC1cuPCO/5+kRmq3906KFi0qm82m0NBQ/f3332nqAb9kyZLWVTvh4eF66aWX7J5K4ebmpqFDh+q1116zbs3YsmXLPT9F4HZ/N6UbV1bNmTNH4eHhj9wXLiVKlNC1a9f06aef6o8//tBXX32l6dOnZ3VZDxTCAaRZly5ddPnyZVWvXl19+vRR//79rUfZpaRKlSr69ttvNX/+fFWoUEHDhw/XO++8k+IjXm6nf//+8vDw0Pvvvy/pxn1j77//vl566SX99ddf97tJSEFGvM6zZs1S1apV9eSTTyowMFDGGP3888/JLgGTbjyr9ptvvlH58uXVqFGjO97Tl3Q52MN2X9zD7KWXXtLTTz+t9u3bq0aNGvr333/triJIL61atdLAgQMVEhKiypUra/PmzXr77bft2rRt21ZNmzZVw4YNlS9fPuvxT+PGjdOqVatUuHBhPf7445JuPMLIx8dHtWrVUsuWLRUcHKwqVaqke92O6qOPPlLdunXVsmVLBQUFqU6dOqpatao1fdy4cSpcuLDq1q2rTp066dVXX7W7jDNHjhzasGGDihQpoqefflply5ZVjx49dOXKFetKghdffFGff/65Zs2apYoVK6p+/fqaPXv2bS97T0lCQoL69OmjsmXLqmnTpipVqpTd4xAdlZeXlzZs2KDmzZurVKlSeuuttzRu3Dg1a9ZMktSzZ0+VLl1a1apVU758+bRp06Z7PkdtNpt+/vln1atXT927d1ep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",
      "text/plain": [
       "<Figure size 1200x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "\n",
    "\n",
    "# Plotting the corrected bar chart\n",
    "plt.figure(figsize=(12, 6))  # Set the figure size\n",
    "sns.barplot(\n",
    "    x='borough', \n",
    "    y='kwh_consumption', \n",
    "    data= energy_clean_textual_data,  # Corrected DataFrame\n",
    "    color='maroon'  # Optional: Set bar color\n",
    ")\n",
    "\n",
    "# Labeling the axes and providing a title\n",
    "plt.xlabel(\"Borough\")\n",
    "plt.ylabel(\"kWh Consumption\")  # Corrected typo\n",
    "plt.title(\"Comparison of kWh Consumption Across Boroughs\")\n",
    "\n",
    "# Display the plot\n",
    "plt.show()  # This should render the bar chart without errors\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 102,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>borough</th>\n",
       "      <th>account_name</th>\n",
       "      <th>serial_number</th>\n",
       "      <th>funding_origin</th>\n",
       "      <th>total_bill</th>\n",
       "      <th>kwh_consumption</th>\n",
       "      <th>kwh_bill</th>\n",
       "      <th>kw_consumption</th>\n",
       "      <th>kw_bill</th>\n",
       "      <th>year_month</th>\n",
       "      <th>start_date</th>\n",
       "      <th>end_date</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>15396.82</td>\n",
       "      <td>128800.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-01-01</td>\n",
       "      <td>2009-12-24</td>\n",
       "      <td>2010-01-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>14556.34</td>\n",
       "      <td>115200.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>224.0</td>\n",
       "      <td>2912.0</td>\n",
       "      <td>2010-02-01</td>\n",
       "      <td>2010-01-26</td>\n",
       "      <td>2010-02-25</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>13904.98</td>\n",
       "      <td>103200.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-03-01</td>\n",
       "      <td>2010-02-25</td>\n",
       "      <td>2010-03-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>14764.04</td>\n",
       "      <td>105600.0</td>\n",
       "      <td>2704.0</td>\n",
       "      <td>208.0</td>\n",
       "      <td>2704.0</td>\n",
       "      <td>2010-04-01</td>\n",
       "      <td>2010-03-26</td>\n",
       "      <td>2010-04-26</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>bronx</td>\n",
       "      <td>adams</td>\n",
       "      <td>7223256</td>\n",
       "      <td>federal</td>\n",
       "      <td>13729.54</td>\n",
       "      <td>97600.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>216.0</td>\n",
       "      <td>2808.0</td>\n",
       "      <td>2010-05-01</td>\n",
       "      <td>2010-04-26</td>\n",
       "      <td>2010-05-24</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "  borough account_name serial_number funding_origin  total_bill  \\\n",
       "0   bronx        adams       7223256        federal    15396.82   \n",
       "1   bronx        adams       7223256        federal    14556.34   \n",
       "2   bronx        adams       7223256        federal    13904.98   \n",
       "3   bronx        adams       7223256        federal    14764.04   \n",
       "4   bronx        adams       7223256        federal    13729.54   \n",
       "\n",
       "   kwh_consumption  kwh_bill  kw_consumption  kw_bill year_month start_date  \\\n",
       "0         128800.0    2808.0           216.0   2808.0 2010-01-01 2009-12-24   \n",
       "1         115200.0    2912.0           224.0   2912.0 2010-02-01 2010-01-26   \n",
       "2         103200.0    2808.0           216.0   2808.0 2010-03-01 2010-02-25   \n",
       "3         105600.0    2704.0           208.0   2704.0 2010-04-01 2010-03-26   \n",
       "4          97600.0    2808.0           216.0   2808.0 2010-05-01 2010-04-26   \n",
       "\n",
       "    end_date  \n",
       "0 2010-01-26  \n",
       "1 2010-02-25  \n",
       "2 2010-03-26  \n",
       "3 2010-04-26  \n",
       "4 2010-05-24  "
      ]
     },
     "execution_count": 102,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_clean_textual_data.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 105,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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1KiBrl274tSpUwCA27dvIy8vD9WqVTM4r1q1agXW+T5ozpw5cHNz0z9q1KhRptdBRERERJZj1SUNpqpfvz7q16+vf92+fXtcvXoVH3/8Mb7++muz2w0LC0NoaKj+dWpqKoNeIiIiIhvxWAW8hWnbti2OHDkCAKhcuTLs7OyQmJhoUCcxMRFeXl5FtqFWq6FWq8u0n0RERERkHY/VkobCxMbGwtvbGwDg4OCAVq1aITIyUn9cq9UiMjIS/v7+1uoiEREREVmRVWd409PTceXKFf3ra9euITY2Fp6enqhZsybCwsLwzz//YN26dQCAJUuWwM/PD40bN0ZWVhZWrVqFAwcOYO/evfo2QkNDERwcjNatW6Nt27ZYsmQJMjIy9FkbiIiIiOjJYtWA98SJE+jWrZv+tW4dbXBwMCIiIhAfH48bN27oj+fk5OD999/HP//8A2dnZzRr1gz79+83aGPQoEH4999/MXXqVCQkJKBFixbYs2dPgRvZiIiIiOjJoBBCCGt3orxJTU2Fm5sbUlJS4Orqau3uEBEREdFDTInXHvs1vERERERExWHAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNMY8BIRERGRTWPAS0REREQ2jQEvEREREdk0BrxEREREZNOsGvAePnwYffr0gY+PDxQKBbZv315s/a1bt+K5555DlSpV4OrqCn9/f/z8888GdaZNmwaFQmHwaNCgQRleBRERERGVZ1YNeDMyMtC8eXMsW7bMqPqHDx/G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vC+//DKqV6+O9u3bY8+ePXj22Wfx008/4fbt29i2bVtp99Fm6ALcb78F/vtf4MYNYMYMeWOan598njFDlv/3v8B33+Wf5+4OpKYCa9YAn3/OrYWJiIiIjGVWlgalUonKlStj2LBh+M9//oOOHTvC2dm5LPpnFWWVpSEzUz68vORSheeek+tyO3UCKlYE0tKAX34Bli0D9u3Lz8jg6Cg3nWjeHHjhBWZpICIiIirzLA137tzBqlWrkJOTg7CwMFSuXBnt27fHxIkTsXfvXrM6/STQavN3WhMC2LsX6NtXZmBQqeRz376yXIj8jAxaLTBihAyEmaWBiIiIyDSlkof3ypUrmDVrFr799ltotVrutFaE0sjDK0R+mVpdal0jIiIieqyUyU5rD7pz5w4OHTqEqKgoREVF4cKFC3B3d0efPn3QpUsXszr9JHiUndb695fB7oNlRERERFQyswLeqlWronLlyujUqRNGjBiBrl27omnTpqXdN5uj0cibzwBAoQB69JCZGDp3zl/De/iwXLKgW9bg7i7P27YN6NcPuHw5v4wzvEREREQlM2sNb3h4OBITE7F582aMHTvWINgdP358qXXO1uTmypnaevWAuDggIkIub+jWDahbVz7HxsryuDiZc7d/f3nezp0yJdnTT8vd15ilgYiIiMg4Zq3hdXd3x/r16wvk3H3vvfewYcMGxMfHl1oHraGs1vBmZQH378vNJ1avBqZMKTyfrkoFzJwJDBsmMzU4OsoMDcOHA717A97ezNJARERET7Yyz9Lw7bffYsiQIThy5Ii+bOzYsfj+++9x8OBBc5p8Ijg4yOA1IgKYMKHozSM0Gnl87Vq5bCEjAzh6VL6uWhVwcrJot4mIiIgea2YFvL169cLy5cvx/PPP4+TJkxg9ejS2bt2KgwcPokGDBqXdR5uRkyNneSdNMq7+xImy/oEDcqZ3xw7giy/kDDERERERGcesm9YAudtacnIyOnTogCpVquDQoUOoW7duafbN5uTl5efhNYZGI3dV69oVWLFC3uAWHy+DXyIiIiIyjtFreENDQwst37RpE5555hnUqVNHX7Z48eLS6Z2VlLc8vEeOyMwMt27JbYdbtACUZs3NExEREdmGMsnDe/r06ULL69ati9TUVP1xhUJhQlefLObm4XV0zJ/tffdduTTC0bEMOkhERERkg4wOeHkz2qN7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",
      "text/plain": [
       "<Figure size 800x600 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "# Create a scatter plot of kW_consumption vs. kWh_consumption\n",
    "plt.figure(figsize=(8, 6))  # Set plot size\n",
    "sns.scatterplot(x='kw_consumption', y='kwh_consumption', data= energy_clean_textual_data, color='b', s=100)  # Scatter plot with blue dots and larger size\n",
    "\n",
    "# Set axis labels and plot title\n",
    "plt.xlabel(\"kw_consumption\")\n",
    "plt.ylabel(\"kwh_consumption\")\n",
    "plt.title(\"Scatter Plot of kWh vs. kW for Each Building\")\n",
    "\n",
    "# Display the plot\n",
    "plt.show()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "energy_40 = energy_selected_column.head(40)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# # Connection parameters\n",
    "# conn_params = {\n",
    "#     'dbname': 'nyc_energy',\n",
    "#     'user': 'postgres',\n",
    "#     'password': 'postgres',         \n",
    "#     'host': 'localhost',\n",
    "#     'port': '5432'\n",
    "# }\n",
    "\n",
    "# # Connect to the PostgreSQL database\n",
    "# conn = psycopg2.connect(**conn_params)\n",
    "# cur = conn.cursor()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# # Create the 'nyc_energy database\n",
    "# cur.execute(\"CREATE DATABASE  nyc_energy\")\n",
    "\n",
    "# # Commit the changes and close the connection to the default database\n",
    "# conn.commit()\n",
    "# cur.close()\n",
    "# conn.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "borough             object\n",
       "account_name        object\n",
       "serial_number       object\n",
       "funding_origin      object\n",
       "total_bill         float64\n",
       "kwh_consumption    float64\n",
       "kwh_bill           float64\n",
       "kw_consumption     float64\n",
       "kw_bill            float64\n",
       "billing_month       object\n",
       "bill_start_date     object\n",
       "bill_end_date       object\n",
       "dtype: object"
      ]
     },
     "execution_count": 154,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_40.dtypes"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 40 entries, 0 to 39\n",
      "Data columns (total 12 columns):\n",
      " #   Column           Non-Null Count  Dtype  \n",
      "---  ------           --------------  -----  \n",
      " 0   borough          40 non-null     object \n",
      " 1   account_name     40 non-null     object \n",
      " 2   serial_number    40 non-null     object \n",
      " 3   funding_origin   40 non-null     object \n",
      " 4   total_bill       40 non-null     float64\n",
      " 5   kwh_consumption  40 non-null     float64\n",
      " 6   kwh_bill         40 non-null     float64\n",
      " 7   kw_consumption   40 non-null     float64\n",
      " 8   kw_bill          40 non-null     float64\n",
      " 9   billing_month    40 non-null     object \n",
      " 10  bill_start_date  40 non-null     object \n",
      " 11  bill_end_date    40 non-null     object \n",
      "dtypes: float64(5), object(7)\n",
      "memory usage: 3.9+ KB\n"
     ]
    }
   ],
   "source": [
    "energy_40.info()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## load dataframe into postgres\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "ename": "OperationalError",
     "evalue": "FATAL:  password authentication failed for user \"postgres\"\n",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mOperationalError\u001b[0m                          Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[156], line 7\u001b[0m\n\u001b[1;32m      3\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mpsycopg2\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m extras\n\u001b[1;32m      6\u001b[0m  \u001b[38;5;66;03m# Connect to PostgreSQL\u001b[39;00m\n\u001b[0;32m----> 7\u001b[0m conn \u001b[38;5;241m=\u001b[39m \u001b[43mpsycopg2\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mconnect\u001b[49m\u001b[43m(\u001b[49m\n\u001b[1;32m      8\u001b[0m \u001b[43m    \u001b[49m\u001b[43mdbname\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mnyc_energy\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[1;32m      9\u001b[0m \u001b[43m    \u001b[49m\u001b[43muser\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mpostgres\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[1;32m     10\u001b[0m \u001b[43m    \u001b[49m\u001b[43mpassword\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mpostgres\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[1;32m     11\u001b[0m \u001b[43m    \u001b[49m\u001b[43mhost\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43mlocalhost\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[43m,\u001b[49m\n\u001b[1;32m     12\u001b[0m \u001b[43m    \u001b[49m\u001b[43mport\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\u001b[38;5;124;43m5432\u001b[39;49m\u001b[38;5;124;43m'\u001b[39;49m\n\u001b[1;32m     13\u001b[0m \u001b[43m)\u001b[49m\n\u001b[1;32m     15\u001b[0m \u001b[38;5;66;03m# Create a cursor for database operations\u001b[39;00m\n\u001b[1;32m     16\u001b[0m cur \u001b[38;5;241m=\u001b[39m conn\u001b[38;5;241m.\u001b[39mcursor()\n",
      "File \u001b[0;32m~/Documents/DS-TKH/repo/nyc_energy_consumption/venv/lib/python3.11/site-packages/psycopg2/__init__.py:122\u001b[0m, in \u001b[0;36mconnect\u001b[0;34m(dsn, connection_factory, cursor_factory, **kwargs)\u001b[0m\n\u001b[1;32m    119\u001b[0m     kwasync[\u001b[38;5;124m'\u001b[39m\u001b[38;5;124masync_\u001b[39m\u001b[38;5;124m'\u001b[39m] \u001b[38;5;241m=\u001b[39m kwargs\u001b[38;5;241m.\u001b[39mpop(\u001b[38;5;124m'\u001b[39m\u001b[38;5;124masync_\u001b[39m\u001b[38;5;124m'\u001b[39m)\n\u001b[1;32m    121\u001b[0m dsn \u001b[38;5;241m=\u001b[39m _ext\u001b[38;5;241m.\u001b[39mmake_dsn(dsn, \u001b[38;5;241m*\u001b[39m\u001b[38;5;241m*\u001b[39mkwargs)\n\u001b[0;32m--> 122\u001b[0m conn \u001b[38;5;241m=\u001b[39m \u001b[43m_connect\u001b[49m\u001b[43m(\u001b[49m\u001b[43mdsn\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[43mconnection_factory\u001b[49m\u001b[38;5;241;43m=\u001b[39;49m\u001b[43mconnection_factory\u001b[49m\u001b[43m,\u001b[49m\u001b[43m \u001b[49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[38;5;241;43m*\u001b[39;49m\u001b[43mkwasync\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m    123\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m cursor_factory \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[1;32m    124\u001b[0m     conn\u001b[38;5;241m.\u001b[39mcursor_factory \u001b[38;5;241m=\u001b[39m cursor_factory\n",
      "\u001b[0;31mOperationalError\u001b[0m: FATAL:  password authentication failed for user \"postgres\"\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import psycopg2\n",
    "from psycopg2 import extras\n",
    "\n",
    "\n",
    " # Connect to PostgreSQL\n",
    "conn = psycopg2.connect(\n",
    "    dbname='nyc_energy',\n",
    "    user='postgres',\n",
    "    password='postgres',\n",
    "    host='localhost',\n",
    "    port='5432'\n",
    ")\n",
    "\n",
    "# Create a cursor for database operations\n",
    "cur = conn.cursor()\n",
    "\n",
    "# Define the PostgreSQL table structure (if needed)\n",
    "create_table_query = \"\"\"\n",
    "CREATE TABLE IF NOT EXISTS raw_energy_data (\n",
    "    id SERIAL PRIMARY KEY,\n",
    "    borough VARCHAR(100),\n",
    "    account_name VARCHAR(100),\n",
    "    funding_source VARCHAR(100), \n",
    "    meter_number INT,\n",
    "    revenue_month DATE,\n",
    "    service_end_date DATE,\n",
    "    service_start_date DATE,\n",
    "    tds_number FLOAT,\n",
    "    current_charges FLOAT\n",
    ")\n",
    "\"\"\"\n",
    "cur.execute(create_table_query)\n",
    "\n",
    "# Define the insertion query for bulk insertion\n",
    "insert_query = \"\"\"\n",
    "INSERT INTO raw_energy_data (borough, account_name, funding_source, meter_number, revenue_month, service_end_date, service_start_date, tds_number, current_charges) VALUES %s\n",
    "\"\"\"\n",
    "\n",
    "# Define the insertion query for bulk insertion\n",
    "values = [tuple(row) for row in energy_40[['borough', 'account_name', 'funding_source', 'meter_number', 'revenue_month', 'service_end_date', 'service_start_date', 'tds_number', 'current_charges']].values]\n",
    "\n",
    "# Execute the insertion query with corrected values\n",
    "extras.execute_values(cur, insert_query, values)\n",
    "\n",
    "# Commit changes\n",
    "conn.commit()\n",
    "\n",
    "# Close the cursor and connection\n",
    "cur.close()\n",
    "conn.close()\n",
    "\n",
    "print(\"Data inserted successfully.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "array([['BRONX', '7223256'],\n",
       "       ['BRONX', '7223256'],\n",
       "       ['BRONX', '7223256'],\n",
       "       ...,\n",
       "       ['BROOKLYN', '2786583'],\n",
       "       ['BROOKLYN', '2786584'],\n",
       "       ['BROOKLYN', '2786586']], dtype=object)"
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "energy_selected_column[['borough', 'meter_number']].values"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256'),\n",
       " ('BRONX', '7223256')]"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "[tuple(row) for row in energy_selected_column[['borough', 'meter_number']].head(10).values]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
