import glob
import os
import shutil
import time
from time import sleep

import sys
from selenium import webdriver


def clear(directory):
    """
    Elimina todos los archivos del directorio
    :param directory: directorio
    :return:
    """
    os.chdir(directory)
    for file in os.listdir(directory):
        if os.path.isfile(file):
            os.remove(directory + "/" + file)


def save(input_dir, output_dir, number, timeout=50):
    """
    Mueve los archivos y los enumera: {numero}.xls
    :param input_dir: directorio donde se encuentra el archivo .xls
    :param output_dir: directorio donde se movera el archivo
    :param name: nombre del archivo
    :return:
    """
    counter = 0
    # espera que exista el archivo, ya que la descarga demora
    while (len(glob.glob(input_dir + "/*.xls")) == 0) and (counter < timeout):
        print("waiting")
        sleep(1)
        counter += 1

    if counter == timeout:
        return

    # creamos la carpeta sino existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("saved")

    for src in glob.glob(input_dir + "/*.xls"):
        dst = output_dir + "/" + str(number) + ".xls"
        print(dst)
        # mueve el archivo hacia su destino con el nuevo nombre
        shutil.move(src, dst)


if __name__ == '__main__':
    location = "/home/qhipa/Downloads"
    output_dr = "/home/qhipa/out"

    clear(location)

    chromedriver = '/usr/bin/chromedriver'
    url = "http://app20.susalud.gob.pe:8080/registro-renipress-webapp/listadoEstablecimientosRegistrados.htm" \
          "?action=mostrarBuscar#"
    chrome = webdriver.PhantomJS("/usr/bin/phantomjs") #webdriver.Chrome(chromedriver)
    chrome.get(url)
    time.sleep(5)  # Let the user actually see something! (5 seconds)
    # Filtering
    print("Filtering")
    elem_estado = chrome.find_element_by_xpath('//*[@id="cmb_estado"]/option[1]')
    elem_estado.click()  # para tener a eess activos y no activos
    print("clicked")
    numbers = list(range(1, 482))
    numbers.remove(24)
    numbers.remove(50)
    for number in numbers:
        print(number)
        elem_servicio = chrome.find_element_by_xpath(
            '//*[@id="div-cabecera-buscar"]/div[2]/div[1]/div[3]/div[3]/div/select/option[{number}]'.format(number=number))
        elem_servicio.click()
        print(number)
        try:
            elem_buscar = chrome.find_element_by_xpath('//*[@id="btnBuscar"]/i')
            elem_buscar.click()  # para tener mostrar la base seleccionada

            time.sleep(5)  # Let the user actually see something! (5 seconds)
            chrome.execute_script("document.getElementById('datable-grilla-establecimientos-renipress_btnExpAux').click();")
            save(location, output_dr, number, timeout=500)

        except:
            print(sys.exc_info()[0])

    chrome.quit()
