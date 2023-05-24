import os
import datasets

logger = datasets.logging.get_logger(__name__)
_DESCRIPTION = """\\nWikipedia-based Image Text (WIT) Dataset is a large multimodal multilingual dataset. 
WIT is composed of a curated set of 37.6 million entity rich image-text examples with 11.5 million unique images across 108 Wikipedia languages. 
Its size enables WIT to be used as a pretraining dataset for multimodal machine learning models.
"""
_CITATION = """
@article{srinivasan2021wit,
  title={WIT: Wikipedia-based Image Text Dataset for Multimodal Multilingual Machine Learning},
  author={Srinivasan, Krishna and Raman, Karthik and Chen, Jiecao and Bendersky, Michael and Najork, Marc},
  journal={arXiv preprint arXiv:2103.01913},
  year={2021}
}
"""
_URL = "https://github.com/google-research-datasets/wit"
_DATA_URL = "https://huggingface.co/datasets/keshan/wit-dataset/resolve/628260b88f51c831a60120d2ebc17c3475f282af/data/{language}.tar.gz"
_LANGUAGES = [
              'ms',
              'eu',
              'si',
              'ko',
              'nv',
              'id',
              'tg',
              'mn',
              'fa',
              'bg',
              'ia',
              'ca',
              'jv',
              'vi',
              'ja',
              'bs',
              'te',
              'war',
              'hy',
              'sv',
              'az',
              'lah',
              'ht',
              'sl',
              'pt',
              'an',
              'br',
              'nn',
              'ceb',
              'ce',
              'qu',
              'gl',
              'fy',
              'vec',
              'zh',
              'iw',
              'vo',
              'xmf',
              'nds',
              'bar',
              'ba',
              'sr-Latn',
              'hsb',
              'yue',
              'arz',
              'es',
              'bn',
              'de',
              'mk',
              'pa',
              'zh-TW',
              'io',
              'lb',
              'azb',
              'ga',
              'cs',
              'fi',
              'cv',
              'sr',
              'lv',
              'my',
              'mg',
              'hu',
              'it',
              'kk',
              'be',
              'sq',
              'ru',
              'ar',
              'cy',
              'hr',
              'be-tarask',
              'is',
              'tt',
              'mr',
              'ro',
              'en',
              'fil',
              'uz',
              'af',
              'et',
              'fr',
              'no',
              'ckb',
              'nan',
              'sw',
              'la',
              'lmo',
              'th',
              'ta',
              'ast',
              'eo',
              'tr',
              'uk',
              'ur',
              'ne',
              'kn',
              'da',
              'nl',
              'ka',
              'pl',
              'el',
              'sco',
              'hi',
              'sk',
              'oc',
              'lt',
              'ml'
              ]

class WITConfig(datasets.BuilderConfig):
    """BuilderConfig for WIT."""
    def __init__(self, *args, languages, **kwargs):
        """BuilderConfig for WIT.
        Args:
            languages (:obj:`List[str]`): list of languages to load
            **kwargs: keyword arguments forwarded to super.
        """
        super().__init__(
            *args,
            name="+".join(languages),
            **kwargs,
        )
        self.languages = languages

class WIT(datasets.GeneratorBasedBuilder):
    """WIT, WIT to be used as a pretraining dataset for multimodal machine learning models."""
    BUILDER_CONFIGS = [WITConfig(languages=[lang]) for lang in _LANGUAGES]
    BUILDER_CONFIG_CLASS = WITConfig
    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "language": datasets.Value("string"),
                    "page_url": datasets.Value("string"),
                    "image_url": datasets.Value("string"),
                    "page_title": datasets.Value("string"),
                    "section_title": datasets.Value("string"),
                    "hierarchical_section_title": datasets.Value("string"),
                    "caption_reference_description": datasets.Value("string"),
                    "caption_attribution_description": datasets.Value("string"),
                    "caption_alt_text_description": datasets.Value("string"),
                    "mime_type": datasets.Value("string"),
                    "original_height": datasets.Value("string"),#datasets.Value("int8"),
                    "original_width": datasets.Value("string"),#datasets.Value("int8"),
                    "is_main_image": datasets.Value("string"),
                    "attribution_passes_lang_id": datasets.Value("string"),
                    "page_changed_recently": datasets.Value("string"),
                    "context_page_description": datasets.Value("string"),
                    "context_section_description": datasets.Value("string"),
                }
            ),
            supervised_keys=None,
            homepage=_URL,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        abs_path_to_data = dl_manager.download_and_extract(
            _DATA_URL.format(language=self.config.name)
            )
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "filepath": os.path.join(abs_path_to_data, f'{self.config.name}/wit_v1.train.all.{self.config.name}.tsv'),
                },
            ),
        ]
    
    def _generate_examples(self, filepath):
      data_fields = list(self._info().features.keys())
      path_idx = data_fields.index("image_url")
      
      with open(filepath, encoding="utf-8") as f:
          lines = f.readlines()
          headline = lines[0]

          column_names = headline.strip().split('\t')
          assert (
                column_names == data_fields
            ), f"The file should have {data_fields} as column names, but has {column_names}"

          for id_, line in enumerate(lines[1:]):
            field_values = line.strip().split("\t")
            # if data is incomplete, fill with empty values
            if len(field_values) < len(data_fields):
                field_values += (len(data_fields) - len(field_values)) * ["''"]

            yield id_, {key: value for key, value in zip(data_fields, field_values)}