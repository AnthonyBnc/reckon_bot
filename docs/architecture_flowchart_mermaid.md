# Architecture Flowchart

```mermaid
flowchart TD
    A[User] --> B[Streamlit App]
    B --> C[Text Preference]
    B --> D[Image Upload]
    B --> E[Voice Recording]
    D --> F[Azure AI Vision]
    F --> G[Caption, Tags, Objects, OCR]
    E --> H[Azure Speech to Text]
    H --> I[Transcript]
    C --> J[Combined Search Profile]
    G --> J
    I --> J
    J --> K[Keyword Processing]
    K --> L[Recipe CSV]
    L --> M[Recommendation Scoring]
    K --> M
    M --> N[Ranked Recipes and Explanation]
```
