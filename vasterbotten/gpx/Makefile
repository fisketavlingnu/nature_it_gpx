#------------------------------------------------------------
#   Copyright 2024 Outdoor Recreation Sverige
#   All Rights Reserved Worldwide
#
#   Licensed under the Apache License, Version 2.0 (the
#   "License"); you may not use this file except in
#   compliance with the License.  You may obtain a copy of
#   the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in
#   writing, software distributed under the License is
#   distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#   CONDITIONS OF ANY KIND, either express or implied.  See
#   the License for the specific language governing
#   permissions and limitations under the License.
#------------------------------------------------------------

clean:
	@rm -f *.gpx *~

KMLFILE=../kml_from_lansstyrelsen/Smavilt_jaktomr_2014_S99.kml


all:komplett VS VN VA SU RAN GRAN

komplett:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output hela_vasterbotten.gpx -area "Alla områden i Västerbotten"

VS:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Vilhelmina_Sodra_VS.gpx -filter VS -area "Vilhelmina Södra Sameby"

VN:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Vilhelmina_Norra_VN.gpx -filter VN -area "Vilhelmina Norra Sameby"

VA:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Storuman_Vapsten_VA.gpx -filter VA -area "Vapsten Sameby"

SU:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Storuman_Ubmeje_U.gpx -filter U -area "Ubmeje Sameby"

RAN:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Sorsele_Ran_R.gpx -filter R -area "Ran Sameby"

GRAN:
	@../../scripts/kml2gpx.py -file ${KMLFILE} -output Sorsele_Gran_G.gpx -filter G -area "Gran Sameby"
