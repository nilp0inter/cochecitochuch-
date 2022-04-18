#include "motor.h"
#include "esp_event.h"
#include "driver/ledc.h"
#include "esp_log.h"
#include "driver/gpio.h"


#define BLINK_GPIO 2

#define ESP_INTR_FLAG_DEFAULT 0
#define GPIO_IR  34
#define GPIO_INPUT_PIN_SEL  1ULL<<GPIO_IR

static const char *TAG = "example";
static uint8_t s_led_state = 0;


static int duty_cycle = LEDC_DUTY;
static int duty_step = 100;
int64_t tv_now;

static void blink_led(void)
{
    s_led_state = !s_led_state;
    /* Set the GPIO level according to the state (LOW or HIGH)*/
    gpio_set_level(BLINK_GPIO, s_led_state);
}


void IRHandler(void *arg){
    if (esp_timer_get_time() - tv_now > 1000) {
        blink_led();
        duty_cycle = duty_cycle + duty_step;
        ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, duty_cycle);
        ledc_update_duty(LEDC_MODE, LEDC_CHANNEL);
    }
}



void app_main(void)
{
    esp_timer_early_init();
    gpio_reset_pin(BLINK_GPIO);
    gpio_set_direction(BLINK_GPIO, GPIO_MODE_DEF_OUTPUT);

    //zero-initialize the config structure.
    gpio_config_t io_conf = {};

    //interrupt of rising edge
    io_conf.intr_type = GPIO_INTR_POSEDGE;
    //bit mask of the pins, use GPIO4/5 here
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    //set as input mode
    io_conf.mode = GPIO_MODE_INPUT;
    //enable pull-up mode
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);
    tv_now = esp_timer_get_time();

    gpio_set_intr_type(GPIO_IR, GPIO_INTR_ANYEDGE);

    ESP_LOGI(TAG, "isr service installation %d", gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT));
    ESP_LOGI(TAG, "isr handler installation %d", gpio_isr_handler_add(GPIO_IR, IRHandler, (void*) GPIO_IR));

    motor_main();
}