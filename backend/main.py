import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE' 
import uvicorn
from presentations.fastapi_app import app


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()