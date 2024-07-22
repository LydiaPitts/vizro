import pandas as pd
import pytest
from langchain_core.messages import HumanMessage
from vizro_ai.dashboard.graph.dashboard_creation import GraphState
from vizro_ai.dashboard.utils import DfMetadata, MetadataContent


@pytest.fixture
def dataframes():
    return [pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [4, 5, 6, 7, 8]})]


@pytest.fixture
def df_metadata():
    df_metadata = DfMetadata({})
    df_metadata.metadata["gdp_chart"] = MetadataContent(
        df_schema={"a": "int64", "b": "int64"},
        df=pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [4, 5, 6, 7, 8]}),
        df_sample=pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": [4, 5, 6, 7, 8]}),
    )
    return df_metadata


@pytest.fixture
def graph_state(dataframes, df_metadata):
    return GraphState(
        messages=[HumanMessage(content="contents of the message")], dfs=dataframes, df_metadata=df_metadata, pages=[]
    )