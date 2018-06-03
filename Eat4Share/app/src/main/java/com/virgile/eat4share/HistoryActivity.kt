package com.virgile.eat4share

import android.databinding.ObservableArrayList
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.support.v7.widget.LinearLayoutManager
import com.github.nitrico.lastadapter.LastAdapter
import kotlinx.android.synthetic.main.activity_history.*

class HistoryActivity : AppCompatActivity() {
    private var history = HistoryItemsViewModel()
    private var historyItems: ArrayList<HistoryItem>? = null

    private fun createFakeHistory(): ArrayList<HistoryItem> {
        var historyItems = ArrayList<HistoryItem>()
        val historyItem = HistoryItem()

        historyItem.restaurantName = "Les Jardins de l'Espadon\n\nRitz Paris"
        historyItem.restaurantDescription = "Cadre prestigieux, service simplet et convivial, cuisine parfaite. Tout est parfait, par exemple les cannellonis ou la raviole végétale en entrée, le bar ou le merlan, le pigeon ou le ris de veau. Cuisson parfaites, chair fondante et peau craquante, un délice !"
        historyItem.restaurantAdress = "15 Place Vendôme, 75001 Paris"
        historyItem.restaurantRatingStars = 5
        historyItem.restaurantNote = 10

        for (i: Int in 0..10) {
            historyItems.add(historyItem)
        }
        return historyItems
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_history)

        historyRv.layoutManager = LinearLayoutManager(baseContext)

        LastAdapter(history.items, 1)
                .map<HistoryHeaderViewModel>(R.layout.fragment_history_feedback_header)
                .map<HistoryLeftItemViewModel>(R.layout.fragment_history_feedback_align_left)
                .map<HistoryRightItemViewModel>(R.layout.fragment_history_feedback_align_right)
                .into(historyRv)

        historyItems = createFakeHistory()
        history.setHistoryItems(historyItems)
    }
}

class HistoryItem {
    var restaurantName: String? = null
    var restaurantAdress: String? = null
    var restaurantRatingStars: Int? = 0
    var restaurantNote: Int? = 0
    var restaurantDescription: String? = null
}

class HistoryItemsViewModel() {
    var items = ObservableArrayList<Any>()

    fun setHistoryItems(historyItem: ArrayList<HistoryItem>?) {
        var leftSide = true
        items.add(HistoryHeaderViewModel())
        historyItem!!.forEach {
            if (leftSide)
                items.add(HistoryLeftItemViewModel(it))
            else
                items.add(HistoryRightItemViewModel(it))
            leftSide = !leftSide
        }
    }
}

class HistoryHeaderViewModel

data class HistoryLeftItemViewModel(val historyItem: HistoryItem) {
    val restaurantName by lazy { historyItem.restaurantName }
    val restaurantAdress by lazy { historyItem.restaurantAdress }
    val restaurantRatingStars by lazy { historyItem.restaurantRatingStars }
    val restaurantNote by lazy { historyItem.restaurantNote.toString() + " / 10" }
    val restaurantDescription by lazy { historyItem.restaurantDescription }


}

data class HistoryRightItemViewModel(val historyItem: HistoryItem) {
    val restaurantName by lazy { historyItem.restaurantName }
    val restaurantAdress by lazy { historyItem.restaurantAdress }
    val restaurantRatingStars by lazy { historyItem.restaurantRatingStars }
    val restaurantNote by lazy { historyItem.restaurantNote.toString() + " / 10" }
    val restaurantDescription by lazy { historyItem.restaurantDescription }

}

